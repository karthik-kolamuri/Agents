from agno import Task
from app.tools.lead_tools import persist_lead
from app.tools.calendar_tools import book_calendar_slot
from app.tools.notification_tools import send_intake_packet, notify_staff
from app.tools.audit_tools import write_audit_log
from app.policies.eligibility_policy import check_eligibility

capture_lead = Task(
    name="capture_lead",
    tool=persist_lead,
    retries=3,
    timeout=5
)

eligibility_check = Task(
    name="eligibility_check",
    tool=check_eligibility,
    depends_on=["capture_lead"]
)

book_consult = Task(
    name="book_consult",
    tool=book_calendar_slot,
    depends_on=["eligibility_check"],
    condition=lambda ctx: ctx["eligibility_check"]["eligible"] is True
)

send_packet = Task(
    name="send_intake_packet",
    tool=send_intake_packet,
    depends_on=["book_consult"]
)

notify = Task(
    name="notify_staff",
    tool=notify_staff,
    depends_on=["book_consult"]
)

audit = Task(
    name="audit_log",
    tool=write_audit_log,
    depends_on=[
        "capture_lead",
        "eligibility_check",
        "book_consult"
    ]
)
