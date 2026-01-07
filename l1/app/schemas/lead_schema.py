# app/schemas/lead_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional # <--- Add this import

class LeadInput(BaseModel):
    name: str
    contact: str
    matter_type: str
    jurisdiction: str
    urgency: str
    # Change it to Optional with a default value of None
    preferred_time: Optional[datetime] = None