from datetime import datetime, timedelta
import os.path
from app.config import settings

# Placeholder for Google API imports (to be installed via requirements.txt)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    pass # Handled if in Mock Mode

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_creds():
    """Authenticates and returns Google API credentials."""
    creds = None
    # Try loading from token.json (User OAuth)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print(" [DEBUG] Using User Credentials (token.json)")
    
    # If no valid user token, try Service Account
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print(" [DEBUG] Refreshed User Credentials")
        elif os.path.exists(settings.GOOGLE_APPLICATION_CREDENTIALS):
            try:
                from google.oauth2 import service_account
                creds = service_account.Credentials.from_service_account_file(
                    settings.GOOGLE_APPLICATION_CREDENTIALS, scopes=SCOPES
                )
                print(" [DEBUG] Using Service Account Credentials (google_credentials.json)")
                print(" [WARNING] Service Accounts cannot access Gmail/User Sheets. Run setup_auth.py if you need these.")
            except ValueError:
                print(" [ERROR] Failed to load 'google_credentials.json' as a Service Account.")
                print(" [TIP] It looks like you are using an OAuth Client ID (Good!). Please run 'python Agents/LegalIntakeMVP/setup_auth.py' to generate token.json.")
                return None
        else:
            print(" [ERROR] No credentials found!")
            return None
            
    return creds

def book_consultation(client_name: str, preferred_time: str) -> str:
    """
    Books a consultation on Google Calendar.
    Args:
        client_name: Name of the client.
        preferred_time: ISO format string of the preferred time.
    """
    if settings.MOCK_MODE:
        print(f"\n[MOCK] 📅 Google Calendar: Booked consultation for {client_name} at {preferred_time}")
        return "success_mock_booking_id_123"

    try:
        creds = get_creds()
        if not creds:
             return "error: credentials not found"
        
        service = build('calendar', 'v3', credentials=creds)
        start_time = datetime.fromisoformat(preferred_time)
        end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': f'Legal Consultation: {client_name}',
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"success_booking_id_{event.get('id')}"
    except Exception as e:
        return f"error: {str(e)}"

def log_lead_to_sheet(name: str, contact: str, matter_type: str, jurisdiction: str, urgency: str, parties: list, preferred_time: str = None) -> str:
    """
    Logs lead details to a Google Sheet.
    Args:
        name: Full name of the client.
        contact: Contact information.
        matter_type: Type of legal matter.
        jurisdiction: Jurisdiction/Location.
        urgency: Urgency level.
        parties: Involved parties.
        preferred_time: Preferred consultation time (optional).
    """
    if settings.MOCK_MODE:
        pt_str = f" | {preferred_time}" if preferred_time else ""
        parties_str = ", ".join(parties) if isinstance(parties, list) else str(parties)
        print(f"\n[MOCK] 📝 Google Sheets: Appended row -> {name} | {contact} | {matter_type} | {parties_str}{pt_str}")
        return "success_mock_row_added"

    try:
        creds = get_creds()
        if not creds:
             return "error: credentials not found"
             
        service = build('sheets', 'v4', credentials=creds)
        
        # Prepare row data
        parties_str = ", ".join(parties) if isinstance(parties, list) else str(parties)
        values = [[name, contact, matter_type, jurisdiction, urgency, parties_str, preferred_time or ""]]
        body = {'values': values}
        
        result = service.spreadsheets().values().append(
            spreadsheetId=settings.GOOGLE_SHEET_ID,
            range='Sheet1!A:G',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        return f"success_row_added_{result.get('updates').get('updatedCells')}"
    except Exception as e:
        return f"error: {str(e)}"

def send_email(to_email: str, subject: str, body: str) -> str:
    """
    Sends an email via Gmail.
    """
    if settings.MOCK_MODE:
        print(f"\n[MOCK] 📧 Gmail: Sent email to {to_email} | Subject: {subject}\nBody: {body[:50]}...")
        return "success_mock_email_sent"
    
    try:
        creds = get_creds()
        if not creds:
             return "error: credentials not found"
             
        service = build('gmail', 'v1', credentials=creds)
        
        from email.mime.text import MIMEText
        from base64 import urlsafe_b64encode
        
        message = MIMEText(body)
        message['to'] = "karthik.kolamuri@sasi.ac.in"
        message['subject'] = subject
        raw_message = urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        msg = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        return f"success_email_sent_{msg['id']}"
    except Exception as e:
        return f"error: {str(e)}"
