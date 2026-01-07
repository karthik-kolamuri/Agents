from datetime import datetime
from app.agents.l1_legal_intake_agent import L1_LEGAL_INTAKE_AGENT
from app.schemas.lead_schema import LeadInput

lead = LeadInput(
    name="Ramesh Kumar",
    contact="+91XXXXXXXXXX",
    matter_type="property",
    jurisdiction="Bangalore",
    urgency="high",
    preferred_time=datetime(2026, 1, 20, 11, 0)
)

result = L1_LEGAL_INTAKE_AGENT.run(lead)
print(result)
# The agent (L1_LEGAL_INTAKE_AGENT) is not instantiated in this file.
# It is imported from 'app.agents.l1_legal_intake_agent', where it is created.

