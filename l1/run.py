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



# run.py
import os
from dotenv import load_dotenv
load_dotenv() # This loads the variables from .env
from datetime import datetime # <--- Add this import
from app.agents.l1_legal_intake_agent import L1_LEGAL_INTAKE_AGENT
from app.schemas.lead_schema import LeadInput

lead_data = LeadInput(
    name='Ramesh Kumar', 
    contact='+91XXXXXXXXXX', 
    matter_type='property', 
    jurisdiction='Bangalore', 
    urgency='high',
    preferred_time=datetime(2026, 1, 20, 11, 0) # <--- Add this field
)

L1_LEGAL_INTAKE_AGENT.print_response(lead_data)