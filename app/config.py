import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

DB_PATH = "data/nordia.db"
APP_NAME = "Nordia WhatsApp IA"
PORT = int(os.getenv("PORT", "8000"))

# WhatsApp Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "976165072250440")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v22.0")

# Token health status
TOKEN_IS_VALID = False
TOKEN_INVALID_SINCE = None  # Timestamp when token was detected as invalid

def validate_whatsapp_token():
    """
    Healthcheck: Validates WhatsApp token by calling Graph API /me endpoint
    Returns True if token is valid, False otherwise
    """
    global TOKEN_IS_VALID, TOKEN_INVALID_SINCE

    if not WHATSAPP_TOKEN:
        print("[CONFIG] ✗ WHATSAPP_TOKEN not set - Running in DEGRADED MODE (receive only)")
        TOKEN_IS_VALID = False
        TOKEN_INVALID_SINCE = datetime.now()
        return False

    # Log token load (without exposing full token)
    token_preview = f"{WHATSAPP_TOKEN[:10]}...{WHATSAPP_TOKEN[-10:]}" if len(WHATSAPP_TOKEN) > 20 else "***"
    print(f"[CONFIG] ✓ WHATSAPP_TOKEN loaded: {token_preview} (length: {len(WHATSAPP_TOKEN)})")

    # Validate token against Graph API using /me endpoint (more stable than /{PHONE_ID})
    try:
        url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/me"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

        print(f"[CONFIG] Validating token with Graph API /me endpoint...")
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f"[CONFIG] ✓ Token validated successfully")
            TOKEN_IS_VALID = True
            TOKEN_INVALID_SINCE = None  # Clear timestamp on successful validation
            return True
        elif response.status_code == 401:
            error_data = response.json()
            error_msg = error_data.get("error", {})
            TOKEN_IS_VALID = False
            TOKEN_INVALID_SINCE = datetime.now()
            print(f"[CONFIG] ✗ TOKEN INVALID - Code: {error_msg.get('code')}, Subcode: {error_msg.get('error_subcode')}")
            print(f"[CONFIG] ✗ Message: {error_msg.get('message')}")
            print(f"[CONFIG] ✗ Invalid since: {TOKEN_INVALID_SINCE.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[CONFIG] ⚠️  Running in DEGRADED MODE (receive only)")
            print(f"[CONFIG] ⚠️  ACTION REQUIRED: Generate new token and update WHATSAPP_TOKEN")
            return False
        else:
            TOKEN_IS_VALID = False
            TOKEN_INVALID_SINCE = datetime.now()
            print(f"[CONFIG] ⚠️  Token validation returned {response.status_code}: {response.text}")
            print(f"[CONFIG] ⚠️  Running in DEGRADED MODE (receive only)")
            return False

    except requests.exceptions.Timeout:
        print(f"[CONFIG] ⚠️  Token validation timeout - assuming valid but check connectivity")
        TOKEN_IS_VALID = True  # Assume valid on timeout to avoid false positives
        TOKEN_INVALID_SINCE = None
        return True
    except Exception as e:
        TOKEN_IS_VALID = False
        TOKEN_INVALID_SINCE = datetime.now()
        print(f"[CONFIG] ⚠️  Token validation error: {e}")
        print(f"[CONFIG] ⚠️  Running in DEGRADED MODE (receive only)")
        return False

# Run healthcheck at startup
validate_whatsapp_token()
