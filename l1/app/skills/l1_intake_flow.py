# # app/skills/l1_intake_flow.py
# from agno.skills.skill import Skill
# from app.tools.lead_tools import persist_lead
# from app.tools.calendar_tools import book_calendar_slot
# from app.tools.notification_tools import send_intake_packet, notify_staff
# from app.tools.audit_tools import write_audit_log
# from app.policies.eligibility_policy import check_eligibility
# import os

# class L1IntakeFlow(Skill):
#     def __init__(self):
#         super().__init__(
#             name="l1_intake_flow",
#             description="Legal Intake & Lead Triage workflow",
#             instructions="Take a lead input, check eligibility, book consult, send packet, notify staff, audit log",
#             source_path=os.path.abspath(__file__)
#         )

#     def run(self, lead: dict) -> dict:
#         context = {}
#         context["capture_lead"] = persist_lead(lead)
#         context["eligibility_check"] = check_eligibility(lead)
#         if not context["eligibility_check"]["eligible"]:
#             write_audit_log(context)
#             return {"status": "REJECTED", "reason": context["eligibility_check"]["reason"]}
#         context["book_consult"] = book_calendar_slot(lead)
#         context["send_packet"] = send_intake_packet(lead)
#         context["notify"] = notify_staff(context["book_consult"])
#         context["audit"] = write_audit_log(context)
#         return {
#             "status": "ACCEPTED",
#             "lead_id": context["capture_lead"]["lead_id"],
#             "event_id": context["book_consult"]["event_id"]
#         }

# l1_intake_flow = L1IntakeFlow()  # ✅ Must be a Skill instance





# app/skills/l1_intake_flow.py
from agno.tools import Toolkit # Changed from Skill
from app.tools.lead_tools import persist_lead
from app.tools.calendar_tools import book_calendar_slot
from app.tools.notification_tools import send_intake_packet, notify_staff
from app.tools.audit_tools import write_audit_log
from app.policies.eligibility_policy import check_eligibility

class L1IntakeFlow(Toolkit):
    def __init__(self):
        super().__init__(name="l1_intake_flow")
        # Register the function so the Agent can see it
        self.register(self.run_l1_flow)

    def run_l1_flow(self, lead: dict) -> dict:
        """
        Executes the legal intake workflow. 
        It persists the lead, checks eligibility, books a calendar slot, 
        sends an intake packet, and notifies staff.
        
        :param lead: Dictionary containing name, contact, matter_type, jurisdiction, and urgency.
        :return: A dictionary with the status (ACCEPTED/REJECTED) and relevant IDs.
        """
        context = {}
        context["capture_lead"] = persist_lead(lead)
        context["eligibility_check"] = check_eligibility(lead)
        
        if not context["eligibility_check"]["eligible"]:
            write_audit_log(context)
            return {"status": "REJECTED", "reason": context["eligibility_check"]["reason"]}
        
        context["book_consult"] = book_calendar_slot(lead)
        context["send_packet"] = send_intake_packet(lead)
        context["notify"] = notify_staff(context["book_consult"])
        context["audit"] = write_audit_log(context)
        
        return {
            "status": "ACCEPTED",
            "lead_id": context["capture_lead"]["lead_id"],
            "event_id": context["book_consult"]["event_id"]
        }

l1_intake_flow = L1IntakeFlow()