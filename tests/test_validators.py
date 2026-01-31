"""
Tests for input validation functions.

Following TDD approach: tests written before implementation.
Validates business rules for nombre, horarios, and servicios inputs.
"""

import pytest
from app.validators import validate_nombre, validate_horarios, validate_servicios


# ==================== VALIDATE_NOMBRE TESTS ====================

def test_validate_nombre_valid():
    """Valid business names should pass validation."""
    valid_names = [
        "Barbería El Corte",
        "Café Molido",
        "Pizzería Napoli 123",
        "Gym Fitness",
        "Auto Service 24hs",
        "La Peluquería",
    ]

    for name in valid_names:
        is_valid, error_msg = validate_nombre(name)
        assert is_valid, f"'{name}' should be valid but got: {error_msg}"
        assert error_msg == "", f"Valid name should have empty error message"


def test_validate_nombre_too_short():
    """Names with less than 3 characters should be rejected."""
    invalid_names = ["", "ab", "X"]

    for name in invalid_names:
        is_valid, error_msg = validate_nombre(name)
        assert not is_valid, f"'{name}' should be invalid (too short)"
        assert "3 caracteres" in error_msg
        assert "al menos" in error_msg.lower()


def test_validate_nombre_too_long():
    """Names longer than 50 characters should be rejected."""
    long_name = "X" * 51
    is_valid, error_msg = validate_nombre(long_name)

    assert not is_valid
    assert "50 caracteres" in error_msg
    assert "máximo" in error_msg.lower()


def test_validate_nombre_only_numbers():
    """Names with only numbers should be rejected."""
    invalid_names = ["123", "456789", "999"]

    for name in invalid_names:
        is_valid, error_msg = validate_nombre(name)
        assert not is_valid, f"'{name}' should be invalid (only numbers)"
        assert "solo números" in error_msg.lower()


def test_validate_nombre_no_letters():
    """Names without any letters should be rejected."""
    # Note: pure numbers are tested separately in test_validate_nombre_only_numbers
    invalid_names = ["!!!", "---", "$$$"]

    for name in invalid_names:
        is_valid, error_msg = validate_nombre(name)
        assert not is_valid, f"'{name}' should be invalid (no letters)"
        assert "letra" in error_msg.lower()


def test_validate_nombre_with_spaces_and_special_chars():
    """Names with spaces and special chars should be valid if they meet other criteria."""
    valid_names = [
        "Café & Bar",
        "La Barbería",
        "Auto-Service",
        "Gym 24/7",
        "Peluquería D'Juan"
    ]

    for name in valid_names:
        is_valid, error_msg = validate_nombre(name)
        assert is_valid, f"'{name}' should be valid"


# ==================== VALIDATE_HORARIOS TESTS ====================

def test_validate_horarios_valid():
    """Valid horarios should pass validation."""
    valid_horarios = [
        "Lun-Vie 9-18hs",
        "9-17hs",
        "24hs",
        "Lunes a Viernes 8am-5pm",
        "7-22 todos los días",
        "L-V 9-13 y 15-19",
    ]

    for horario in valid_horarios:
        is_valid, error_msg = validate_horarios(horario)
        assert is_valid, f"'{horario}' should be valid but got: {error_msg}"
        assert error_msg == ""


def test_validate_horarios_too_short():
    """Horarios with less than 3 characters should be rejected."""
    invalid_horarios = ["", "9", "ab"]

    for horario in invalid_horarios:
        is_valid, error_msg = validate_horarios(horario)
        assert not is_valid, f"'{horario}' should be invalid (too short)"
        assert "3 caracteres" in error_msg
        assert "al menos" in error_msg.lower()


def test_validate_horarios_no_numbers():
    """Horarios without numbers should be rejected."""
    invalid_horarios = ["todo el día", "always", "xxx"]

    for horario in invalid_horarios:
        is_valid, error_msg = validate_horarios(horario)
        assert not is_valid, f"'{horario}' should be invalid (no numbers)"
        assert "números" in error_msg.lower()


def test_validate_horarios_no_letters():
    """Horarios without letters should be rejected."""
    invalid_horarios = ["9-18", "123", "00:00"]

    for horario in invalid_horarios:
        is_valid, error_msg = validate_horarios(horario)
        assert not is_valid, f"'{horario}' should be invalid (no letters)"
        assert "letras" in error_msg.lower()


# ==================== VALIDATE_SERVICIOS TESTS ====================

def test_validate_servicios_valid():
    """Valid servicios should pass validation."""
    valid_servicios = [
        "Corte $5000",
        "corte $8000, barba $5000",
        "Café y medialunas $1500",
        "Musculación $3000/mes",
        "Alineación $2500, balanceo $1800",
        "Pizza grande $3500"
    ]

    for servicio in valid_servicios:
        is_valid, error_msg = validate_servicios(servicio)
        assert is_valid, f"'{servicio}' should be valid but got: {error_msg}"
        assert error_msg == ""


def test_validate_servicios_too_short():
    """Servicios with less than 3 characters should be rejected."""
    invalid_servicios = ["", "ab", "X"]

    for servicio in invalid_servicios:
        is_valid, error_msg = validate_servicios(servicio)
        assert not is_valid, f"'{servicio}' should be invalid (too short)"
        assert "3 caracteres" in error_msg
        assert "al menos" in error_msg.lower()


def test_validate_servicios_no_numbers():
    """Servicios without numbers (prices) should be rejected."""
    invalid_servicios = ["corte y barba", "café", "todo"]

    for servicio in invalid_servicios:
        is_valid, error_msg = validate_servicios(servicio)
        assert not is_valid, f"'{servicio}' should be invalid (no numbers)"
        assert "precios" in error_msg.lower()


def test_validate_servicios_no_letters():
    """Servicios without letters (service names) should be rejected."""
    # These have numbers but no letters
    invalid_servicios = ["5000", "123-456", "$9999"]

    for servicio in invalid_servicios:
        is_valid, error_msg = validate_servicios(servicio)
        assert not is_valid, f"'{servicio}' should be invalid (no letters)"
        assert "nombres" in error_msg.lower()
