from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.config import APP_NAME
from app import engine, whatsapp

app = FastAPI(title=APP_NAME)

class WebhookMessage(BaseModel):
    from_: str = Field(alias="from")
    message: str

    model_config = {"populate_by_name": True}

@app.get("/")
def healthcheck():
    return {"status": "ok", "app": APP_NAME}

@app.post("/webhook")
def webhook(msg: WebhookMessage):
    phone = msg.from_
    text = msg.message

    response = engine.process_message(phone, text)
    whatsapp.send_message(phone, response)

    return {"status": "ok"}
