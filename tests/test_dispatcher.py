"""
Tests for Signal Dispatcher (Layer 0) - Plane Classification.

Tests the dispatch_signal function that classifies messages into
ADMIN or CUSTOMER planes based on sender identity, state, and commands.
"""

import pytest
from app.dispatcher import dispatch_signal


def test_admin_with_command_returns_admin():
    """
    Admin whitelisted number + admin command → ADMIN plane
    """
    sender = "5493794281273"
    text = "/setup"
    current_state = "inicial"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "ADMIN"


def test_admin_with_keyword_without_slash_returns_admin():
    """
    Admin whitelisted number + admin keyword (no slash) → ADMIN plane
    """
    sender = "5493794281273"
    text = "activar cliente"
    current_state = "inicial"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "ADMIN"


def test_admin_with_normal_text_returns_customer():
    """
    Admin whitelisted number + normal text (no command) → CUSTOMER plane
    """
    sender = "5493794281273"
    text = "hola"
    current_state = "inicial"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "CUSTOMER"


def test_non_admin_with_command_returns_customer():
    """
    Non-whitelisted number + admin command → CUSTOMER plane
    (Identity check blocks them)
    """
    sender = "5491155551234"
    text = "/setup"
    current_state = "inicial"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "CUSTOMER"


def test_continuity_activation_flow_returns_admin():
    """
    Any sender in activation state → ADMIN plane
    (Continuity check - preserve admin flow)
    """
    sender = "5491155551234"  # Non-admin number
    text = "Juan Pérez"
    current_state = "activation_awaiting_name"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "ADMIN"


def test_continuity_setup_flow_returns_admin():
    """
    Any sender in setup state → ADMIN plane
    (Continuity check - preserve admin flow)
    """
    sender = "5491155551234"  # Non-admin number
    text = "Lun-Vie 9-18"
    current_state = "esperando_horarios"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "ADMIN"


def test_customer_state_returns_customer():
    """
    Any sender in customer state (completado) → CUSTOMER plane
    """
    sender = "5491155551234"
    text = "hola"
    current_state = "completado"

    plane = dispatch_signal(sender, text, current_state)

    assert plane == "CUSTOMER"
