def send_intake_packet(lead: dict) -> dict:
    return {
        "packet_url": "https://secure.example.com/intake",
        "sent": True
    }

def notify_staff(event: dict) -> dict:
    return {
        "staff_notified": True,
        "channel": "internal"
    }
