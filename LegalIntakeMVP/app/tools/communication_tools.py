from app.config import settings

# Placeholder for Twilio imports
try:
    from twilio.rest import Client
except ImportError:
    pass

def send_whatsapp(to_number: str, message: str) -> str:
    """
    Sends a WhatsApp message via Twilio.
    Args:
        to_number: The recipient's phone number (e.g., +1234567890).
        message: The text message content.
    """
    if settings.MOCK_MODE:
        print(f"\n[MOCK] 💬 WhatsApp: Sent to {to_number}: \"{message}\"")
        return "success_mock_message_sid"

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # Twilio whatsapp numbers require 'whatsapp:' prefix
        from_ = settings.TWILIO_FROM_NUMBER
        # Remove spaces and ensure strict format
        clean_number = to_number.replace(" ", "").strip()
        to_ = f"whatsapp:{clean_number}" if not clean_number.startswith("whatsapp:") else clean_number
        
        msg = client.messages.create(
            body=message,
            from_=from_,
            to=to_
        )
        return msg.sid
    except Exception as e:
        return f"error: {str(e)}"
