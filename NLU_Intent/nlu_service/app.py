import os
from typing import Any, Dict, List, Optional
import json
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

from fastapi import FastAPI
from pydantic import BaseModel

from .agent import nlu_intent_agent
from .qa_search import QASearcher

load_dotenv()

app = FastAPI(title="NLU & Intent Detection Service")
searcher = QASearcher()

class Utterance(BaseModel):
    speaker: str
    text: str

class AnalyzeRequest(BaseModel):
    session_id: str
    caller_id: str
    utterance: str
    turn_index: int
    detected_language: Optional[str] = None
    context: List[Utterance] = []

class AnalyzeResponse(BaseModel):
    session_id: str
    turn_index: int
    intent: str
    intent_confidence: float
    language: str
    entities: Dict[str, Any]
    answer_text: str
    qa_match: Optional[Dict[str, Any]] = None
    flags: Dict[str, bool] = {"escalate_to_human": False, "small_talk": False}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    if nlu_intent_agent.model is None:
        # Fallback if no GROQ_API_KEY is configured.
        return AnalyzeResponse(
            session_id=req.session_id,
            turn_index=req.turn_index,
            intent="PROJECT_INFO",
            intent_confidence=0.0,
            language=req.detected_language or "unknown",
            entities={},
            answer_text="NLU agent is not configured with an LLM model yet.",
            qa_match=None,
            flags={"escalate_to_human": True, "small_talk": False},
        )

    # Prepare a compact input payload for the agent.
    agent_input = {
        "session_id": req.session_id,
        "caller_id": req.caller_id,
        "utterance": req.utterance,
        "turn_index": req.turn_index,
        "detected_language": req.detected_language,
        "context": [{"speaker": c.speaker, "text": c.text} for c in req.context],
    }

    # Run agent turn (Session history is handled automatically by PostgresDb)
    raw = nlu_intent_agent.run(agent_input, session_id=req.session_id)
    # Agent is instructed to return pure JSON.
    data = json.loads(str(raw))

    qa_category = data.get("qa_category") or data.get("intent") or "PROJECT_INFO"
    qa_match = searcher.best_match(req.utterance, qa_category=qa_category)

    if qa_match:
        answer_text = qa_match["answer"]
    else:
        answer_text = data.get("answer_text", "")

    flags = {
        "escalate_to_human": bool(data.get("escalate_to_human", False)),
        "small_talk": False,
    }

    return AnalyzeResponse(
        session_id=req.session_id,
        turn_index=req.turn_index,
        intent=data.get("intent", "PROJECT_INFO"),
        intent_confidence=float(data.get("intent_confidence", 0.0)),
        language=data.get("language", req.detected_language or "unknown"),
        entities=data.get("entities", {}) or {},
        answer_text=answer_text,
        qa_match=qa_match,
        flags=flags,
    )


