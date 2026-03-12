import os
from typing import Any, Dict, List, Optional
import json
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row # Keeping for potential future use if needed, but unused now

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from pydantic import BaseModel

from .agent import nlu_intent_agent
from .qa_search import QASearcher

load_dotenv()

app = FastAPI(title="NLU & Intent Detection Service")
searcher = QASearcher()

# In-memory cache to track collected entities across turns (fallback for DB issues)
session_entity_cache: Dict[str, Dict[str, Any]] = {}

class Utterance(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    session_id: str
    user_id: str
    utterance: str
    detected_language: Optional[str] = None
    context: List[Utterance] = []

class AnalyzeResponse(BaseModel):
    session_id: str
    intent: str
    intent_confidence: float
    language: str
    entities: Dict[str, Any]
    action: str = "SEARCH"
    needs_info: bool = False
    answer_text: str
    qa_match: Optional[Dict[str, Any]] = None
    flags: Dict[str, bool] = {"escalate_to_human": False, "small_talk": False}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    return process_utterance(req)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"[INFO] WebSocket connection accepted")
    try:
        while True:
            data = await websocket.receive_json()
            # Validate payload
            req = AnalyzeRequest(**data)
            # Run processing to get the response Object
            response = await asyncio.to_thread(process_utterance, req)
            # Send result back IMMEDIATELY so STT gets it fast
            await websocket.send_json(response.model_dump())
            
            # Now, run the slow database update in the background
            asyncio.create_task(asyncio.to_thread(update_nlu_db, req, response))
    except WebSocketDisconnect:
        print(f"[INFO] WebSocket disconnected for session {data.get('session_id', 'unknown') if 'data' in locals() else 'unknown'}")
    except Exception as e:
        print(f"[ERROR] WebSocket error: {e}")
        try:
             await websocket.close()
        except:
             pass

def process_utterance(req: AnalyzeRequest) -> AnalyzeResponse:
    if nlu_intent_agent.model is None:
        # Fallback if no GROQ_API_KEY is configured.
        return AnalyzeResponse(
            session_id=req.session_id,
            intent="PROJECT_INFO",
            intent_confidence=0.0,
            language=req.detected_language or "unknown",
            entities={},
            answer_text="NLU agent is not configured with an LLM model yet.",
            qa_match=None,
            flags={"escalate_to_human": True, "small_talk": False},
        )

    # Build a plain-text message for the agent
    context_lines = ""
    if req.context:
        context_lines = "\nRecent context:\n" + "\n".join(
            [f"  {c.speaker}: {c.text}" for c in req.context]
        )

    agent_message = f"Caller utterance: {req.utterance}"
    if req.detected_language:
        agent_message += f"\nDetected language: {req.detected_language}"
        
    # Inject previously collected entities so the agent remembers
    existing_entities = session_entity_cache.get(req.session_id, {})
    if existing_entities:
        agent_message += f"\nPreviously collected information (Do NOT ask for these again): {json.dumps(existing_entities)}"
        
    if context_lines:
        agent_message += context_lines

    # Run agent turn (Session history is handled automatically by PostgresDb)
    raw = nlu_intent_agent.run(agent_message, session_id=req.session_id)
    
    # Agent is instructed to return pure JSON.
    # The return type is a RunResponse object — actual content is in .content
    content_str = ""
    if hasattr(raw, "content") and raw.content:
        content_str = raw.content
    elif hasattr(raw, "messages") and raw.messages:
        # Fallback: scan messages for the last assistant reply with content
        for msg in reversed(raw.messages):
            if hasattr(msg, "role") and msg.role == "assistant" and msg.content:
                content_str = msg.content
                break
    
    # print(f"[DEBUG] Raw agent response type: {type(raw)}")
    # print(f"[DEBUG] Extracted content_str: {repr(content_str)}")

    # Extract JSON robustly: find the first '{' and last '}'
    start_idx = content_str.find('{')
    end_idx = content_str.rfind('}')
    
    if start_idx != -1 and end_idx != -1:
        content_str = content_str[start_idx:end_idx+1]
    
    try:
        data = json.loads(content_str)
    except Exception as e:
        print(f"[WARN] Failed to parse JSON from agent (falling back to similarity search): {e}")
        # Fallback: skip intent extraction, go straight to similarity search
        qa_match = searcher.best_match(req.utterance)
        return AnalyzeResponse(
            session_id=req.session_id,
            intent="PROJECT_INFO",
            intent_confidence=0.0,
            language=req.detected_language or "unknown",
            entities={},
            needs_info=False,
            answer_text=qa_match["answer"] if qa_match else "Sorry, I couldn't process that. Could you rephrase?",
            qa_match=qa_match,
            flags={"escalate_to_human": False, "small_talk": False},
        )

    needs_info = bool(data.get("needs_info", False))
    action = data.get("action", "SEARCH")  # Default to SEARCH for safety

    # Route based on the agent's action decision
    qa_match = None
    answer_text = data.get("answer_text", "")

    if action == "SEARCH" and not needs_info:
        # Only run vector search when agent says SEARCH and has all entities
        qa_category = data.get("qa_category") or data.get("intent") or "PROJECT_INFO"
        qa_match = searcher.best_match(req.utterance, qa_category=qa_category)
        if qa_match:
            answer_text = qa_match["answer"]
        elif not answer_text:
            answer_text = "I'm having trouble accessing our project details right now, but I'm still here to help! What else would you like to discuss?"
    # For CHAT and ASK actions, use the agent's answer_text directly (no vector search)

    flags = {
        "escalate_to_human": bool(data.get("escalate_to_human", False)),
        "small_talk": action == "CHAT",
    }

    # Merge newly detected entities into the session cache
    merged_entities = session_entity_cache.get(req.session_id, {}).copy()
    new_entities = data.get("entities", {}) or {}
    for k, v in new_entities.items():
        if v is not None:
            merged_entities[k] = v
            
    # Save back to cache
    session_entity_cache[req.session_id] = merged_entities

    res = AnalyzeResponse(
        session_id=req.session_id,
        intent=data.get("intent", "OTHER"),
        intent_confidence=float(data.get("intent_confidence", 0.0)),
        language=data.get("language", req.detected_language or "unknown"),
        entities=merged_entities,
        action=action,
        needs_info=needs_info,
        answer_text=answer_text,
        qa_match=qa_match,
        flags=flags,
    )

    return res

def update_nlu_db(req: AnalyzeRequest, res: AnalyzeResponse):
    """Background task to save NLU results to Agent 1's DB"""
    try:
        dsn = os.getenv("DATABASE_URL")
        if not dsn: return
        
        intent_entry = json.dumps({
            "intent": res.intent,
            "confidence": res.intent_confidence,
            "utterance": req.utterance,
            "action": res.action,
            "answer": res.answer_text,
        })
        
        entities_json = json.dumps(res.entities)

        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
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
                    (intent_entry, entities_json, json.dumps(res.language), req.session_id)
                )
    except Exception as e:
        print(f"[WARN] Failed to update Agent 1 calls table: {e}")
