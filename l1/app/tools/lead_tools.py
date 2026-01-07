import uuid
from datetime import datetime

def persist_lead(lead: dict) -> dict:
    return {
        "lead_id": str(uuid.uuid4()),
        "status": "NEW",
        "created_at": datetime.utcnow().isoformat(),
        "lead_payload": lead
    }
