# app/tools/audit_tools.py
import logging
from datetime import datetime

def write_audit_log(event_name: str, details: str) -> dict:
    """
    Records an action or event for legal compliance and audit trails.
    
    Args:
        event_name: The name of the event (e.g., 'LEAD_PERSISTED', 'ELIGIBILITY_CHECK').
        details: A description of what happened or the result of the action.
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] EVENT: {event_name} | DETAILS: {details}"
    
    # In a real industrial app, you'd write this to a database or a secure file
    print(f"--- AUDIT LOG: {log_entry} ---")
    
    return {"status": "logged", "timestamp": timestamp}