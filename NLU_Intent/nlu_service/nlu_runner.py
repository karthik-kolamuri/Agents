import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from .agent import nlu_intent_agent
from .qa_search import QASearcher


load_dotenv()


class NLUIntentEngine:
  """
  Pure agent-style NLU engine (no HTTP routes).

  Usage:

  engine = NLUIntentEngine()
  result = engine.run_turn(
      session_id="abc",
      utterance="What is the price of 2 BHK?",
      language="en",
      context=[{"speaker": "caller", "text": "Hi"}, ...],
  )
  """

  def __init__(self):
    if nlu_intent_agent.model is None:
      raise RuntimeError("NLU agent model is not configured. Set GROQ_API_KEY in environment.")
    self.qa_searcher = QASearcher()

  def run_turn(
    self,
    session_id: str,
    utterance: str,
    language: Optional[str] = None,
    caller_id: Optional[str] = None,
    turn_index: int = 0,
    context: Optional[List[Dict[str, Any]]] = None,
  ) -> Dict[str, Any]:
    """
    Runs one NLU turn and returns a rich result dict suitable for Agent 3.
    """
    if context is None:
      context = []

    agent_input = {
      "session_id": session_id,
      "caller_id": caller_id,
      "utterance": utterance,
      "turn_index": turn_index,
      "detected_language": language,
      "context": context,
    }

    raw = nlu_intent_agent.run(agent_input)
    data = json.loads(str(raw))

    qa_category = data.get("qa_category") or data.get("intent") or "PROJECT_INFO"
    qa_match = self.qa_searcher.best_match(utterance, qa_category=qa_category)

    answer_text = qa_match["answer"]

    result: Dict[str, Any] = {
      "session_id": session_id,
      "turn_index": turn_index,
      "intent": data.get("intent", qa_category),
      "intent_confidence": float(data.get("intent_confidence", 0.0)),
      "language": data.get("language", language or "unknown"),
      "entities": data.get("entities", {}) or {},
      "answer_text": answer_text,
      "qa_match": qa_match,
      "flags": {
        "escalate_to_human": bool(data.get("escalate_to_human", False)),
        "small_talk": False,
      },
    }

    return result

