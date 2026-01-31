"""
Global conversation state management with disk persistence.

This module provides a global conversations dictionary that:
- Persists to disk automatically
- Loads from disk at startup
- Survives FastAPI restarts
"""

from app.persistence import load_state, save_state

# Global conversations state
# Will be loaded from disk at startup
conversaciones = load_state()

print(f"[STATE] Initialized with {len(conversaciones)} conversation(s)")


def update_conversation(phone: str, data: dict) -> None:
    """
    Update conversation state for a phone number and persist to disk.

    Args:
        phone: Phone number (sender)
        data: Dictionary with conversation state

    Usage:
        update_conversation("123456789", {
            "estado": "esperando_nombre",
            "nombre": "Barbería X"
        })
    """
    conversaciones[phone] = data
    save_state(conversaciones)


def get_conversation(phone: str) -> dict:
    """
    Get conversation state for a phone number.

    Args:
        phone: Phone number (sender)

    Returns:
        Conversation dict or empty dict if not found
    """
    return conversaciones.get(phone, {})


def delete_conversation(phone: str) -> None:
    """
    Delete conversation state for a phone number and persist.

    Args:
        phone: Phone number (sender)
    """
    if phone in conversaciones:
        del conversaciones[phone]
        save_state(conversaciones)
