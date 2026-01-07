import uuid

def book_calendar_slot(lead: dict) -> dict:
    return {
        "event_id": str(uuid.uuid4()),
        "scheduled_for": lead["preferred_time"]
    }
