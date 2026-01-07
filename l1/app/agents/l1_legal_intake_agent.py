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



from agno.agent import Agent
# from agno.models.openai import OpenAIChat
# from agno.models.google import Gemini
from agno.models.groq import Groq  # 1. Import Groq


from app.schemas.lead_schema import LeadInput

# Import the atomic tools directly
from app.tools.lead_tools import persist_lead
from app.tools.calendar_tools import book_calendar_slot
from app.tools.notification_tools import send_intake_packet, notify_staff
from app.tools.audit_tools import write_audit_log
from app.policies.eligibility_policy import check_eligibility

# app/agents/l1_legal_intake_agent.py

L1_LEGAL_INTAKE_AGENT = Agent(
    name="L1_Legal_Intake_Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    description="Agentic Legal Intake Specialist",
    input_schema=LeadInput,
    tools=[
        persist_lead, 
        check_eligibility, 
        book_calendar_slot, 
        send_intake_packet, 
        notify_staff, 
        write_audit_log
    ],
    instructions=[
        "You are an expert Legal Intake Specialist.",
        "Always pass arguments to tools as individual fields, not as objects.",
        "Step 1: Persist the lead.",
        "Step 2: Check eligibility.",
        "Step 3: If eligible, book consult, send packet, and notify staff.",
        # Clarify how to use the audit log:
        "IMPORTANT: After every tool call, use 'write_audit_log'.",
        "Pass 'event_name' (e.g., 'Lead Saved') and 'details' (e.g., 'Lead ID: 123 saved successfully') as strings."
    ],
    markdown=True
)