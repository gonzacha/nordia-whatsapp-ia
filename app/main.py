from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
from datetime import datetime
from app.config import APP_NAME, WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_API_VERSION, TOKEN_IS_VALID, TOKEN_INVALID_SINCE
from app.engine import handle_message
from app.state import conversaciones  # Load persisted state
import app.config as config

app = FastAPI(title=APP_NAME)

VERIFY_TOKEN = "nordia_verify_token"

def send_whatsapp_message(to: str, text: str):
    """
    Send WhatsApp message via Cloud API
    DEGRADED MODE: Blocks sending if token is invalid
    """
    if not WHATSAPP_TOKEN:
        print(f"[WhatsApp DEGRADED] No token configured, skipping message to {to}")
        print(f"[WhatsApp DEGRADED] Would have sent: {text}")
        return None

    if not TOKEN_IS_VALID:
        print(f"[WhatsApp DEGRADED] Token invalid/expired - BLOCKING send to {to}")
        print(f"[WhatsApp DEGRADED] Would have sent: {text}")
        print(f"[WhatsApp DEGRADED] ACTION REQUIRED: Update WHATSAPP_TOKEN and restart")
        return None

    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"[DEBUG] Response body: {response.text}")
        response.raise_for_status()
        print(f"[WhatsApp] ✓ Message sent to {to}: {text}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_data = response.json() if response.text else {}
        error_code = error_data.get("error", {}).get("code")
        error_subcode = error_data.get("error", {}).get("error_subcode")

        print(f"[WhatsApp ERROR] HTTP {response.status_code}: {response.text}")

        # Token expiration detection - freeze system immediately
        if response.status_code == 401 and error_code in (190,):
            config.TOKEN_IS_VALID = False
            config.TOKEN_INVALID_SINCE = datetime.now()
            print(f"[WhatsApp CRITICAL] TOKEN EXPIRED - Code: {error_code}, Subcode: {error_subcode}")
            print(f"[WhatsApp CRITICAL] Invalid since: {config.TOKEN_INVALID_SINCE.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[WhatsApp CRITICAL] System entering DEGRADED MODE - blocking all sends")
            print(f"[WhatsApp CRITICAL] Update WHATSAPP_TOKEN immediately to avoid WABA suspension")

        print(f"[WhatsApp ERROR] Failed to send to {to}: {e}")
        return None
    except Exception as e:
        print(f"[WhatsApp ERROR] Failed to send to {to}: {e}")
        return None

@app.get("/")
def healthcheck():
    mode = "operational" if TOKEN_IS_VALID else "degraded"

    whatsapp_status = {
        "token_valid": TOKEN_IS_VALID,
        "can_send": TOKEN_IS_VALID,
        "can_receive": True
    }

    # Include timestamp if token is invalid
    if TOKEN_INVALID_SINCE:
        whatsapp_status["invalid_since"] = TOKEN_INVALID_SINCE.strftime('%Y-%m-%d %H:%M:%S')

    return {
        "status": "ok",
        "app": APP_NAME,
        "mode": mode,
        "whatsapp": whatsapp_status,
        "conversations": {
            "active": len(conversaciones),
            "persisted": True
        }
    }

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    challenge = params.get("hub.challenge")
    token = params.get("hub.verify_token")

    if mode == "subscribe" and token == "nordia_verify_token":
        print("[Webhook] Verified successfully")
        return PlainTextResponse(challenge, status_code=200)

    return PlainTextResponse("Forbidden", status_code=403)

@app.post("/webhook")
async def receive_webhook(payload: dict):
    print("=== WEBHOOK HIT ===")
    print("INCOMING WEBHOOK:", payload)

    try:
        # Extract message data from WhatsApp payload
        entry = payload.get("entry", [])
        if not entry:
            print("[DEBUG] No entry in payload")
            return {"status": "ok"}

        changes = entry[0].get("changes", [])
        if not changes:
            print("[DEBUG] No changes in entry")
            return {"status": "ok"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])

        if not messages:
            print("[DEBUG] No messages in value")
            return {"status": "ok"}

        message = messages[0]
        sender = message.get("from")
        message_type = message.get("type")

        print(f"[Webhook] Message from: {sender}, type: {message_type}")

        # Only respond to text messages
        if message_type == "text":
            text_body = message.get("text", {}).get("body", "")
            print(f"[Webhook] Text received: {text_body}")

            print("=== TRYING TO SEND MESSAGE ===")
            print(f"[DEBUG] Token loaded: {WHATSAPP_TOKEN is not None}")
            print(f"[DEBUG] Token length: {len(WHATSAPP_TOKEN) if WHATSAPP_TOKEN else 0}")
            print(f"[DEBUG] Phone Number ID: {WHATSAPP_PHONE_NUMBER_ID}")

            # Process message through engine
            reply = handle_message(sender, text_body)
            print(f"[ENGINE] Reply => {reply}")

            send_whatsapp_message(sender, reply)

        return {"status": "ok"}

    except Exception as e:
        print(f"[Webhook ERROR] {e}")
        return {"status": "ok"}
