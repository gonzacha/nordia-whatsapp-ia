import requests
from app.config import WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_API_VERSION

def send_message(phone: str, text: str):
    if not WHATSAPP_TOKEN:
        print(f"[WhatsApp STUB] To {phone}: {text}")
        return

    url = f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": text
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"[WhatsApp] Sent to {phone}: {text}")
        return response.json()
    except Exception as e:
        print(f"[WhatsApp ERROR] Failed to send to {phone}: {e}")
        return None
