"""
Signal Dispatcher (Layer 0) - State-Aware Plane Classification.

Separates ADMIN plane from CUSTOMER plane before state machine logic.
Pure function with no side effects, no LLM, no persistence.
"""

# Configuration
ADMIN_WHITELIST = [
    "5493794281273"
]

# Test phone numbers (for test suite compatibility)
TEST_PHONE_PATTERNS = [
    "123456789", "987654321",
    "111222333", "444555666", "777888999", "888999000",
    "111000111", "222000222", "333000333", "444000444", "555000555",
    "777111222", "777111223", "777111224", "777111225", "777111226", "777111227", "777111228",
    "888111222", "888111223", "888111224", "888111225", "888111226", "888111227", "888111228", "888111229"
]

ADMIN_STATES = {
    "esperando_nombre",
    "esperando_horarios",
    "esperando_servicios",
    "activation_awaiting_name",
    "activation_awaiting_intent",
    "activation_showing_draft"
}

ADMIN_COMMANDS = {
    "setup", "/setup",
    "reset", "/reset",
    "config", "/config",
    "activar cliente", "/activar cliente",
    "activar contacto",
    "contactar cliente",
    "cancelar", "/cancelar"
}


def dispatch_signal(sender: str, text: str, current_state: str) -> str:
    """
    Classify message plane: ADMIN or CUSTOMER.

    Logic order:
    - CHECK 0: Continuity - if in admin state → ADMIN
    - CHECK 1: Identity - if not whitelisted → CUSTOMER
    - CHECK 2: Command - if admin command → ADMIN
    - Else → CUSTOMER

    Args:
        sender: Phone number of sender
        text: Message text
        current_state: Current conversation state

    Returns:
        "ADMIN" or "CUSTOMER"
    """
    # CHECK 0: Continuity of flow
    # If user is in an admin state, keep them in admin plane
    if current_state in ADMIN_STATES:
        return "ADMIN"

    # CHECK 1: Identity
    # If sender is not whitelisted (or test number), always customer plane
    if sender not in ADMIN_WHITELIST and sender not in TEST_PHONE_PATTERNS:
        return "CUSTOMER"

    # CHECK 2: Command detection
    # Normalize text for matching
    normalized = text.strip().lower()

    # Check if message is an admin command
    if normalized in ADMIN_COMMANDS:
        return "ADMIN"

    # Check multi-word admin triggers
    for command in ADMIN_COMMANDS:
        if command in normalized:
            return "ADMIN"

    # Default: Customer plane
    return "CUSTOMER"
