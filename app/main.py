from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import requests
from app.config import APP_NAME, WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_API_VERSION

app = FastAPI(title=APP_NAME)

VERIFY_TOKEN = "nordia_verify_token"

def send_whatsapp_message(to: str, text: str):
    """Send WhatsApp message via Cloud API"""
    if not WHATSAPP_TOKEN:
        print(f"[WhatsApp] No token configured, skipping message to {to}")
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
        print(f"[WhatsApp] Message sent to {to}: {text}")
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"[WhatsApp ERROR] HTTP {response.status_code}: {response.text}")
        print(f"[WhatsApp ERROR] Failed to send to {to}: {e}")
        return None
    except Exception as e:
        print(f"[WhatsApp ERROR] Failed to send to {to}: {e}")
        return None

@app.get("/")
def healthcheck():
    return {"status": "ok", "app": APP_NAME}

@app.get("/webhook")
def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge")
):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"[Webhook] Verified successfully")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        print(f"[Webhook] Verification failed")
        return PlainTextResponse(content="Invalid token", status_code=403)

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

            # Send automatic reply
            reply_text = "Hola 👋 Soy Nordia. Escribí 'setup' para comenzar."
            send_whatsapp_message(sender, reply_text)

        return {"status": "ok"}

    except Exception as e:
        print(f"[Webhook ERROR] {e}")
        return {"status": "ok"}
