import os
import sys

print("🚀 Script started...")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    print("✅ Libraries imported successfully.")
except ImportError as e:
    print(f"❌ Error: Missing Dependencies. {e}")
    print("Please run: pip install google-auth google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

# Scopes required by the agent
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.send'
]

def main():
    print("🔍 Checking credentials...")
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("✅ Found existing token.json")
    else:
        print("ℹ️ token.json not found (Normal for first run)")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🚀 Starting new authentication flow...")
            
            if not os.path.exists('google_credentials.json'):
                print("❌ Error: 'google_credentials.json' not found!")
                print("Please download your OAuth 2.0 Client ID JSON from Google Cloud Console and rename it to 'google_credentials.json'.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(
                'google_credentials.json', SCOPES)

            print("🌐 Starting Authentication...")
            print("👇👇👇 ACTION REQUIRED: Copy the long link below (if printed) or check your browser if it opened. 👇👇👇")
            print("-" * 60)
            
            # run_local_server with open_browser=False prints the URL and waits for the localhost callback
            creds = flow.run_local_server(port=0, open_browser=False)
            
            print("-" * 60)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("\n✅ Authentication successful! 'token.json' saved.")
            print("🎉 You are now ready to run the agent!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal Script Error: {e}")
