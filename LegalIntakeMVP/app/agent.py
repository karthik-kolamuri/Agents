from agno.agent import Agent
from agno.models.groq import Groq
from app.config import settings
from app.schemas import LeadInput
from app.tools.google_tools import book_consultation, log_lead_to_sheet, send_email
from app.tools.communication_tools import send_whatsapp

# Define the Legal Intake Agent
legal_intake_agent = Agent(
    name="LegalIntakeMVP",
    model=Groq(id="llama-3.3-70b-versatile", api_key=settings.GROQ_API_KEY),
    description="Automated Legal Intake & Triage Specialist",
    input_schema=None, # Allow flexible string input for now to avoid JSON parsing errors
    tools=[
        log_lead_to_sheet,
        book_consultation,
        send_email,
        send_whatsapp
    ],
    instructions=[
        "You are a Legal Intake Specialist. Your goal is to process new leads efficiently.",
        "Follow this STRICT workflow for every new lead:",
        "1. **Log the Lead**: Use 'log_lead_to_sheet'.",
        "2. **Book Consultation**: If a 'preferred_time' is provided, use tool `book_consultation`.",
        "3. **Send Confirmation**: Use `send_whatsapp`.",
        "4. **Send Intake Packet**: Use `send_email` to the client.",
        f"5. **Notify Staff**: Use `send_email` to '{settings.STAFF_EMAIL}'.",
        "",
        "CRITICAL FOR TOOL USAGE:",
        "- Output ONLY valid JSON for function calls.",
        "- Ensure ALL closures like '}' and ')' are present.",
        "- Do not use trailing commas.",
        "- CAUTION: Do NOT wrap the arguments in a list `[...]` or dictionary `{...}`. Pass them as DIRECT named arguments.",
        "- Strictly follow the tool schema.",
        "Always return a summary of actions taken."
    ],
    markdown=True,
    # show_tool_calls=True
)
