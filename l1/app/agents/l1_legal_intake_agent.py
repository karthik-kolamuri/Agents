# # app/agents/l1_legal_intake_agent.py
# from agno.agent import Agent
# from app.schemas.lead_schema import LeadInput
# from app.skills.l1_intake_flow import l1_intake_flow 

# L1_LEGAL_INTAKE_AGENT = Agent(
#     name="L1_Legal_Intake_Agent",
#     description="Industrial-grade Legal Intake & Lead Triage Agent",
#     input_schema=LeadInput,
#     # Change 'skills' to 'tools' and pass the .run method
#     tools=[l1_intake_flow.run] 
# )




# app/agents/l1_legal_intake_agent.py
from agno.agent import Agent
from app.schemas.lead_schema import LeadInput
from app.skills.l1_intake_flow import l1_intake_flow 

L1_LEGAL_INTAKE_AGENT = Agent(
    name="L1_Legal_Intake_Agent",
    description="Industrial-grade Legal Intake & Lead Triage Agent",
    input_schema=LeadInput,
    tools=[l1_intake_flow], 
    instructions=["Always use the run_l1_flow tool to process incoming lead data."],
    # show_tool_calls=True,  <-- REMOVE OR COMMENT OUT THIS LINE
    markdown=True           # Use this instead to get clean output
)