def send_intake_packet(name: str, contact: str) -> dict:
    """Sends forms to lead. Args: name (str), contact (str)"""
    return {"status": "sent", "link": "https://forms.legal.com/i102"}

def notify_staff(details: str) -> dict:
    """Alerts legal team. Args: details (str)"""
    return {"status": "notified"}