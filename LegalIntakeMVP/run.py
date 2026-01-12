import sys
import os

# Ensure the parent directory is in the path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.config import settings
from app.schemas import LeadInput
from app.agent import legal_intake_agent
from app.agent import legal_intake_agent

if __name__ == "__main__":
    # Sample Lead Data
    sample_lead = LeadInput(
        name="Karthik Kolamuri",
        contact="+91 9182615101",
        matter_type="Criminal Offence",
        jurisdiction="Hyderabad",
        urgency="High",
        parties=["Jane Doe"],
        preferred_time=datetime.now().replace(microsecond=0) + timedelta(days=2)
    )

    print(f"--- 🚀 Starting Legal Intake for: {sample_lead.name} ---")
    print(f"--- ⚙️ MODE: {'MOCK (No Real Actions)' if settings.MOCK_MODE else 'REAL (Live APIs)'} ---")
    
    # Run the agent
    response = legal_intake_agent.run(sample_lead) # Pass the model directly, Agno handles schema validation internally if configured or we pass dict.
    # Note: Agno's .run() usually takes a string prompt or structured input if configured. 
    # Since input_schema is set, passing the pydantic object or dict often works depending on version.
    # For safety with this specific framework version, we'll convert to a prompt-like context or let it handle the object.
    
    # Actually, typically we pass a message. Let's form a structured prompt to be safe.
    prompt = f"""
    Process this new lead:
    Name: {sample_lead.name}
    Contact: {sample_lead.contact}
    Matter: {sample_lead.matter_type}
    Jurisdiction: {sample_lead.jurisdiction}
    Urgency: {sample_lead.urgency}
    Parties: {sample_lead.parties}
    Preferred Time: {sample_lead.preferred_time}
    """
    
    legal_intake_agent.print_response(prompt)
