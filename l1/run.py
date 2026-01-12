from datetime import datetime
# from app.agents.l1_legal_intake_agent import L1_LEGAL_INTAKE_AGENT
# from app.schemas.lead_schema import LeadInput

# if __name__ == "__main__":
#     lead = LeadInput(
#         name="Ramesh Kumar",
#         contact="+91XXXXXXXXXX",
#         matter_type="property",
#         jurisdiction="Bangalore",
#         urgency="high",
#         preferred_time=datetime(2026, 1, 20, 11, 0)
#     )

#     result = L1_LEGAL_INTAKE_AGENT.run(lead)
#     print(result)

import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

from app.agents.l1_legal_intake_agent import L1_LEGAL_INTAKE_AGENT
from app.schemas.lead_schema import LeadInput

lead_data = LeadInput(
    name='Ramesh Kumar', 
    contact='+91XXXXXXXXXX', 
    matter_type='property', 
    jurisdiction='Bangalore', 
    urgency='high',
    parties=['Ramesh Kumar', 'ABC Builders'], # Added parties
    preferred_time=datetime(2026, 2, 20, 11, 0)
)

L1_LEGAL_INTAKE_AGENT.print_response(lead_data)