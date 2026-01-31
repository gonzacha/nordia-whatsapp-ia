"""
Input validation functions for conversational setup flow.

Provides minimal validation for:
- Business name (nombre)
- Business hours (horarios)
- Services offered (servicios)

Each validator returns tuple[bool, str]:
- (True, "") if valid
- (False, "error message") if invalid
"""


def validate_nombre(text: str) -> tuple[bool, str]:
    """
    Validate business name input.

    Rules:
    - Minimum 3 characters
    - Maximum 50 characters
    - Must contain at least one letter
    - Cannot be only numbers

    Args:
        text: User input for business name

    Returns:
        (is_valid, error_message)

    Examples:
        >>> validate_nombre("Barbería El Corte")
        (True, "")
        >>> validate_nombre("ab")
        (False, "El nombre debe tener al menos 3 caracteres.")
        >>> validate_nombre("123")
        (False, "El nombre no puede ser solo números.")
    """
    if len(text) < 3:
        return False, "El nombre debe tener al menos 3 caracteres."

    if len(text) > 50:
        return False, "El nombre debe tener máximo 50 caracteres."

    # Check only-numbers BEFORE checking no-letters (more specific check first)
    if text.isdigit():
        return False, "El nombre no puede ser solo números."

    if not any(c.isalpha() for c in text):
        return False, "El nombre debe contener al menos una letra."

    return True, ""


def validate_horarios(text: str) -> tuple[bool, str]:
    """
    Validate business hours input.

    Rules:
    - Minimum 3 characters
    - Must contain at least one number (time indication)
    - Must contain at least one letter (day/format indication)

    Args:
        text: User input for business hours

    Returns:
        (is_valid, error_message)

    Examples:
        >>> validate_horarios("Lun-Vie 9-18hs")
        (True, "")
        >>> validate_horarios("9-18")
        (False, "Los horarios deben incluir letras (ej: Lun-Vie, hs).")
    """
    if len(text) < 3:
        return False, "Los horarios deben tener al menos 3 caracteres."

    if not any(c.isdigit() for c in text):
        return False, "Los horarios deben incluir números (ej: 9-18hs)."

    if not any(c.isalpha() for c in text):
        return False, "Los horarios deben incluir letras (ej: Lun-Vie, hs)."

    return True, ""


def validate_servicios(text: str) -> tuple[bool, str]:
    """
    Validate services offered input.

    Rules:
    - Minimum 3 characters
    - Must contain at least one number (price indication)
    - Must contain at least one letter (service name)

    Args:
        text: User input for services

    Returns:
        (is_valid, error_message)

    Examples:
        >>> validate_servicios("Corte $5000, barba $3000")
        (True, "")
        >>> validate_servicios("corte y barba")
        (False, "Los servicios deben incluir precios (ej: corte $5000).")
    """
    if len(text) < 3:
        return False, "Los servicios deben tener al menos 3 caracteres."

    if not any(c.isdigit() for c in text):
        return False, "Los servicios deben incluir precios (ej: corte $5000)."

    if not any(c.isalpha() for c in text):
        return False, "Los servicios deben incluir nombres (ej: corte, barba)."

    return True, ""
