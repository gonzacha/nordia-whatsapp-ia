import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/nordia.db"
APP_NAME = "Nordia WhatsApp IA"
PORT = int(os.getenv("PORT", "8000"))
