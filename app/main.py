from fastapi import FastAPI, Request, Query
from app.config import APP_NAME, WHATSAPP_VERIFY_TOKEN
from app import engine, whatsapp

app = FastAPI(title=APP_NAME)

@app.get("/")
def healthcheck():
    return {"status": "ok", "app": APP_NAME}

@app.get("/webhook")
def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge")
):
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        print(f"[Webhook] Verified successfully")
        return int(challenge)
    else:
        print(f"[Webhook] Verification failed")
        return {"error": "verification failed"}, 403

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    try:
        entry = body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ok"}

        message = messages[0]
        phone = message.get("from")
        message_type = message.get("type")

        if message_type == "text":
            text = message.get("text", {}).get("body", "")

            response = engine.process_message(phone, text)
            whatsapp.send_message(phone, response)

        return {"status": "ok"}

    except Exception as e:
        print(f"[Webhook ERROR] {e}")
        return {"status": "error", "message": str(e)}
