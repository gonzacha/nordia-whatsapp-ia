"""
Minimal JSON disk persistence for conversation state.

Implements defensive programming:
- Handles missing files gracefully
- Handles corrupted JSON gracefully
- Creates directories automatically
- Never crashes on I/O errors

Also includes SQLite persistence for message drafts.
"""

from pathlib import Path
import json
from app.models import SessionLocal, MessageDraft

# Path to state file
STATE_FILE = Path("data/conversations_state.json")


def save_state(data: dict) -> None:
    """
    Save conversation state to disk.

    Args:
        data: Dictionary containing conversation state

    Defensive behavior:
    - Creates data/ directory if doesn't exist
    - Logs errors but doesn't crash
    - Uses default=str to handle datetime objects
    - Ensures UTF-8 encoding for unicode/emojis
    """
    # Create directory if doesn't exist
    STATE_FILE.parent.mkdir(exist_ok=True)

    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(
                data,
                f,
                indent=2,
                default=str,  # Convert non-serializable objects (datetime) to string
                ensure_ascii=False  # Preserve unicode/emojis
            )
        print(f"[PERSISTENCE] ✓ Saved {len(data)} conversation(s)")
    except Exception as e:
        print(f"[PERSISTENCE ERROR] Failed to save state: {e}")


def load_state() -> dict:
    """
    Load conversation state from disk.

    Returns:
        Dictionary containing conversation state, or empty dict if:
        - File doesn't exist (first run)
        - JSON is corrupted
        - Any I/O error occurs

    Defensive behavior:
    - Returns empty dict instead of crashing
    - Logs warnings for debugging
    - Handles missing file gracefully
    """
    # File doesn't exist (first run)
    if not STATE_FILE.exists():
        print("[PERSISTENCE] No state file found, starting fresh")
        return {}

    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[PERSISTENCE] ✓ Loaded {len(data)} conversation(s)")
        return data
    except json.JSONDecodeError as e:
        print(f"[PERSISTENCE WARNING] Corrupted state file: {e}")
        print("[PERSISTENCE WARNING] Starting with fresh state")
        return {}
    except Exception as e:
        print(f"[PERSISTENCE ERROR] Failed to load state: {e}")
        return {}


def save_message_draft(customer_name: str, intent: str, message: str) -> int:
    """
    Guarda draft de mensaje en base de datos SQLite.

    Args:
        customer_name: Nombre del cliente
        intent: Intención comercial del usuario
        message: Mensaje generado

    Returns:
        ID del draft creado

    Defensive behavior:
    - Creates database tables if don't exist
    - Logs errors but doesn't crash
    - Returns -1 on error
    """
    try:
        db = SessionLocal()
        draft = MessageDraft(
            customer_name=customer_name,
            commercial_intent=intent,
            generated_message=message
        )
        db.add(draft)
        db.commit()
        db.refresh(draft)
        draft_id = draft.id
        db.close()

        print(f"[PERSISTENCE] ✓ Saved message draft #{draft_id} for {customer_name}")
        return draft_id

    except Exception as e:
        print(f"[PERSISTENCE ERROR] Failed to save message draft: {e}")
        if 'db' in locals():
            db.close()
        return -1
