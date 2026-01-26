import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/nordia.db"
APP_NAME = "Nordia WhatsApp IA"
PORT = int(os.getenv("PORT", "8000"))

# WhatsApp Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "976165072250440")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v22.0")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "nordia_verify_token_123")
