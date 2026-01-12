from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LeadInput(BaseModel):
    name: str = Field(..., description="Full name of the potential client.")
    contact: str = Field(..., description="Phone number or email address.")
    matter_type: str = Field(..., description="Type of legal matter (e.g., 'Divorce', 'Property Dispute').")
    jurisdiction: str = Field(..., description="Location or court jurisdiction.")
    urgency: str = Field(..., description="Urgency level (e.g., 'High', 'Medium', 'Low').")
    parties: List[str] = Field(..., description="List of involved parties (opposing party, etc.).")
    preferred_time: Optional[datetime] = Field(None, description="Preferred consultation time.")
