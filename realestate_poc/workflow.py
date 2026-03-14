import os
import json
import traceback
from typing import Dict, Any, Optional

from agno.workflow import Workflow, Step, StepOutput
from agno.agent import Agent

# Import our custom components
from nlu.agent import nlu_intent_agent
from nlu.qa_search import QASearcher
from tts.agent import generate_and_play_voice
from tools.session_tools import SessionTools

# Instantiate shared tools
searcher = QASearcher()

# In-memory cache for collected entities (simulate persistent state dynamically in the workflow)
session_entity_cache: Dict[str, Dict[str, Any]] = {}

async def context_preparation_step(step_input) -> StepOutput:
    """Prepares the prompt payload for the NLU Agent including historical entities."""
    # Agno wraps arguments in a StepInput object which has an .input attribute
    data = getattr(step_input, "input", step_input)
    if not isinstance(data, dict):
        data = {"utterance": str(data), "session_id": "default"}
        
    utterance = data.get("utterance", "")
    session_id = data.get("session_id", "default_session")
    
    agent_msg = f"Caller utterance: {utterance}\n"
    
    existing_entities = session_entity_cache.get(session_id, {})
    if existing_entities:
        agent_msg += f"\nPreviously collected information (Do NOT ask for these again): {json.dumps(existing_entities)}"
        
    return StepOutput(content={
        "agent_message": agent_msg,
        "session_id": session_id,
        "utterance": utterance
    })

async def nlu_agent_step(step_input) -> StepOutput:
    """Runs the Agno NLU Intent Agent and robustly extracts its JSON response."""
    # step_input.previous_step_content = output from context_preparation_step
    prev = step_input.previous_step_content
    if isinstance(prev, dict) and "agent_message" in prev:
        agent_message = prev["agent_message"]
        session_id = prev["session_id"]
        utterance = prev["utterance"]
    else:
        return StepOutput(content={"error": "Invalid input to NLU step"})
    
    raw = await nlu_intent_agent.arun(agent_message, session_id=session_id)
    
    # Extract JSON content robustly
    content_str = getattr(raw, "content", "")
    if not content_str and hasattr(raw, "messages"):
        for msg in reversed(raw.messages):
            if hasattr(msg, "role") and msg.role == "assistant" and msg.content:
                content_str = msg.content
                break
                
    start_idx = content_str.find('{')
    end_idx = content_str.rfind('}')
    
    parsed_json = {}
    if start_idx != -1 and end_idx != -1:
        content_str = content_str[start_idx:end_idx+1]
        try:
            parsed_json = json.loads(content_str)
        except Exception as e:
            print(f"[WARN] Failed to parse JSON: {e}")
            
    return StepOutput(content={
        "session_id": session_id,
        "utterance": utterance,
        "nlu_data": parsed_json
    })

async def vector_search_step(step_input) -> StepOutput:
    """Executes vector search if NLU requested 'SEARCH', compiles the final answer, and saves to DB."""
    # step_input.previous_step_content = output from nlu_agent_step
    prev = step_input.previous_step_content
    if not isinstance(prev, dict) or "nlu_data" not in prev:
        return StepOutput(content={"error": "Invalid input to vector search step", "answer": "Error"})
        
    session_id = prev["session_id"]
    utterance = prev["utterance"]
    data = prev["nlu_data"]
    
    if not data:
        return StepOutput(content={"error": "No NLU data parsed", "answer": "Sorry, I couldn't process that."})
        
    action = data.get("action", "SEARCH")
    needs_info = bool(data.get("needs_info", False))
    answer_text = data.get("answer_text", "")
    
    qa_match = None
    if action == "SEARCH" and not needs_info:
        qa_category = data.get("qa_category") or data.get("intent") or "PROJECT_INFO"
        # Since QASearcher uses sentence_transformers natively (synchronous CPU compute),
        # we offload it to a thread to prevent blocking the async event loop.
        import asyncio
        qa_match = await asyncio.to_thread(searcher.best_match, utterance, qa_category)
        if qa_match:
            answer_text = qa_match["answer"]
        elif not answer_text:
            answer_text = "I'm having trouble accessing our project details, but I'm still here to help! What else would you like to discuss?"
            
    # Merge entities
    merged_entities = session_entity_cache.get(session_id, {}).copy()
    new_entities = data.get("entities", {}) or {}
    for k, v in new_entities.items():
        if v is not None:
            merged_entities[k] = v
    session_entity_cache[session_id] = merged_entities
    
    final_response = {
        "intent": data.get("intent", "OTHER"),
        "confidence": float(data.get("intent_confidence", 0.0)),
        "action": action,
        "answer": answer_text,
        "entities": merged_entities
    }
    
    # ── Write NLU results back to the "calls" table asynchronously ──
    try:
        import psycopg
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            # Build the intent history entry
            intent_entry = json.dumps({
                "intent": data.get("intent", "OTHER"),
                "confidence": float(data.get("intent_confidence", 0.0)),
                "utterance": utterance,
                "action": action,
                "answer": answer_text,
            })

            # Build merged entities (only non-null values)
            detected_entities = {k: v for k, v in (data.get("entities") or {}).items() if v is not None}
            entities_json = json.dumps(detected_entities)

            # Use asynchronous connection explicitly
            async with await psycopg.AsyncConnection.connect(db_url) as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        UPDATE calls SET
                            session_data = jsonb_set(
                                jsonb_set(
                                    jsonb_set(
                                        session_data,
                                        '{intent_history}',
                                        COALESCE(session_data->'intent_history', '[]'::jsonb) || %s::jsonb
                                    ),
                                    '{entities}',
                                    COALESCE(session_data->'entities', '{}'::jsonb) || %s::jsonb
                                ),
                                '{language}',
                                %s::jsonb
                            )
                        WHERE session_id = %s
                        """,
                        (intent_entry, entities_json, json.dumps(data.get("language", "en")), session_id)
                    )
                    rows_updated = cur.rowcount
                    if rows_updated == 0:
                        print(f"[WARN] No row found in 'calls' for session_id={session_id}")
                    else:
                        print("Saved intent history to DB")
    except Exception as e:
        print(f"[WARN] Failed to update calls table: {e}")
        
    return StepOutput(content=final_response)

async def tts_agent_step(step_input) -> StepOutput:
    """Takes the final answer from the workflow and speaks it aloud using ElevenLabs."""
    prev = step_input.previous_step_content
    if isinstance(prev, dict) and "answer" in prev and prev["answer"]:
        answer_text = prev["answer"]
        # Trigger the voice synthesis in a background asyncio thread
        import asyncio
        loop = asyncio.get_event_loop()
        loop.create_task(generate_and_play_voice(answer_text))
        
    return StepOutput(content=prev)

# Instantiate the final Agno Workflow
realestate_workflow = Workflow(
    name="RealEstate Unified Pipeline",
    steps=[
        context_preparation_step,
        nlu_agent_step,
        vector_search_step,
        tts_agent_step
    ]
)
