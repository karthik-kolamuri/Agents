from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LeadInput(BaseModel):
    name: str = Field(..., description="Full name of the client")
    contact: str = Field(..., description="Phone number or contact info")
    email: str = Field(..., description="Email address of the client")
    matter_type: str = Field(..., description="Type of legal matter (e.g., Family Law, Criminal Defense)")
    jurisdiction: str = Field(..., description="City or State of the issue")
    urgency: str = Field(..., description="Urgency level (e.g., 'High', 'Medium', 'Low').")
    parties: List[str] = Field(..., description="List of involved parties (opposing party, etc.).")
    preferred_time: Optional[datetime] = Field(None, description="Preferred consultation time.")
