from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class LeadInput(BaseModel):
    name: str
    contact: str
    matter_type: Literal["property", "insurance", "legal_consult"]
    jurisdiction: str
    urgency: Literal["low", "medium", "high"]
    preferred_time: datetime
