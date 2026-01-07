from agno import Agent
from app.schemas.lead_schema import LeadInput
from app.tasks.l1_tasks import (
    capture_lead,
    eligibility_check,
    book_consult,
    send_packet,
    notify,
    audit
)

L1_LEGAL_INTAKE_AGENT = Agent(
    name="L1_Legal_Intake_Agent",
    description="""
    Industrial-grade Legal Intake & Lead Triage Agent.

    Responsibilities:
    - Capture lead
    - Apply eligibility policy
    - Book consultation
    - Send intake packet
    - Notify staff
    - Write audit log

    Guarantees:
    - Deterministic
    - Auditable
    - Retry-safe
    """,
    input_schema=LeadInput,
    tasks=[
        capture_lead,
        eligibility_check,
        book_consult,
        send_packet,
        notify,
        audit
    ]
)
