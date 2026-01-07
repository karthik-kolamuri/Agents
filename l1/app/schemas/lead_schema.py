# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional, List

# class LeadInput(BaseModel):
#     name: str
#     contact: str
#     matter_type: str
#     jurisdiction: str
#     urgency: str
#     parties: List[str]  # Added: Client requirement
#     preferred_time: Optional[datetime] = None




from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LeadInput(BaseModel):
    name: str
    contact: str
    matter_type: str
    jurisdiction: str
    urgency: str
    parties: List[str]  # Required by client
    preferred_time: Optional[datetime] = None