"""
Tests for message generation in app/message_generator.py

Tests deterministic message generation:
- Different verb patterns (ofrecer, recordar, invitar, preguntar)
- Fallback for unknown patterns
- Consistent output format
"""

import pytest
from app.message_generator import generate_commercial_message


def test_message_generation_ofrecer():
    """
    Genera mensaje para intent con verbo 'ofrecer'
    """
    msg = generate_commercial_message("Juan", "ofrecer lentes nuevos")

    assert "juan" in msg.lower()
    assert "llegaron nuevos" in msg.lower()
    assert "lentes nuevos" in msg.lower() or "nuevos que te pueden interesar" in msg.lower()
    assert "¿querés que te cuente más?" in msg.lower()


def test_message_generation_recordar():
    """
    Genera mensaje para intent con verbo 'recordar'
    """
    msg = generate_commercial_message("María", "recordar turno del martes")

    assert "maría" in msg.lower()
    assert "recordarte" in msg.lower()
    assert "turno del martes" in msg.lower()
    assert "¿querés que te cuente más?" in msg.lower()


def test_message_generation_invitar():
    """
    Genera mensaje para intent con verbo 'invitar'
    """
    msg = generate_commercial_message("Pedro", "invitar al evento")

    assert "pedro" in msg.lower()
    assert "invitar" in msg.lower()
    assert "evento" in msg.lower()
    assert "¿querés que te cuente más?" in msg.lower()


def test_message_generation_fallback():
    """
    Genera mensaje fallback para intent sin patrón reconocido
    """
    msg = generate_commercial_message("Ana", "xyz random text")

    assert "ana" in msg.lower()
    assert "xyz random text" in msg.lower()
    assert "¿querés que te cuente más?" in msg.lower()
