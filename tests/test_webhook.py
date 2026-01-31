"""
Tests for WhatsApp webhook handling in app/main.py

Tests non-text message handling:
- Image, audio, video, sticker, document, location messages
- Unknown/future message types
- State preservation when non-text received
- Regression test for text messages
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.state import update_conversation, get_conversation, conversaciones

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_test_state():
    """Clean conversation state before each test."""
    conversaciones.clear()
    yield
    conversaciones.clear()


def create_whatsapp_payload(message_type: str, sender: str = "5491112345678"):
    """
    Helper to create WhatsApp Cloud API webhook payload.

    Args:
        message_type: Type of message (text, image, audio, etc.)
        sender: Phone number of sender

    Returns:
        Valid WhatsApp webhook payload dict
    """
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": sender,
                        "type": message_type
                    }]
                }
            }]
        }]
    }

    # Add type-specific data
    if message_type == "text":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"] = {
            "body": "test message"
        }
    elif message_type == "image":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["image"] = {
            "id": "image123"
        }
    elif message_type == "audio":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["audio"] = {
            "id": "audio123"
        }
    elif message_type == "video":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["video"] = {
            "id": "video123"
        }
    elif message_type == "sticker":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["sticker"] = {
            "id": "sticker123"
        }
    elif message_type == "document":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["document"] = {
            "id": "doc123"
        }
    elif message_type == "location":
        payload["entry"][0]["changes"][0]["value"]["messages"][0]["location"] = {
            "latitude": -34.603722,
            "longitude": -58.381592
        }

    return payload


# ==================== NON-TEXT MESSAGE TESTS ====================

@patch('app.main.send_whatsapp_message')
def test_webhook_handles_image_message(mock_send):
    """Image message should trigger generic non-text response."""
    payload = create_whatsapp_payload("image")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    # Verify generic message sent
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args[0][0] == "5491112345678"  # sender
    assert "solo puedo procesar mensajes de texto" in call_args[0][1].lower()
    assert "📝" in call_args[0][1]


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_audio_message(mock_send):
    """Audio message should trigger generic non-text response."""
    payload = create_whatsapp_payload("audio")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert "texto" in call_args[0][1].lower()


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_video_message(mock_send):
    """Video message should trigger generic non-text response."""
    payload = create_whatsapp_payload("video")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_sticker_message(mock_send):
    """Sticker message should trigger generic non-text response."""
    payload = create_whatsapp_payload("sticker")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_document_message(mock_send):
    """Document message should trigger generic non-text response."""
    payload = create_whatsapp_payload("document")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_location_message(mock_send):
    """Location message should trigger generic non-text response."""
    payload = create_whatsapp_payload("location")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()


@patch('app.main.send_whatsapp_message')
def test_webhook_handles_unknown_type(mock_send):
    """Unknown/future message type should trigger generic response."""
    payload = create_whatsapp_payload("future_type_from_whatsapp_2027")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert "texto" in call_args[0][1].lower()


# ==================== STATE PRESERVATION TESTS ====================

@patch('app.main.send_whatsapp_message')
def test_webhook_preserves_state_on_non_text(mock_send):
    """
    Non-text message should NOT modify conversation state.
    User in setup flow should remain in same state.
    """
    sender = "5491187654321"

    # Setup: User in middle of setup flow
    update_conversation(sender, {
        "estado": "esperando_horarios",
        "nombre": "Test Business"
    })

    # User sends image (by accident)
    payload = create_whatsapp_payload("image", sender)
    response = client.post("/webhook", json=payload)

    assert response.status_code == 200

    # Verify state UNCHANGED
    state = get_conversation(sender)
    assert state.get("estado") == "esperando_horarios"
    assert state.get("nombre") == "Test Business"
    assert "horarios" not in state  # Should NOT have advanced

    # Verify generic message sent
    mock_send.assert_called_once()


# ==================== REGRESSION TESTS ====================

@patch('app.main.send_whatsapp_message')
@patch('app.main.handle_message')
def test_webhook_text_message_still_works(mock_handle, mock_send):
    """
    Text messages should still work as before (regression test).
    Feature should NOT break existing text flow.
    """
    mock_handle.return_value = "Bot response"

    payload = create_whatsapp_payload("text")
    response = client.post("/webhook", json=payload)

    assert response.status_code == 200

    # Verify handle_message was called (text processing)
    mock_handle.assert_called_once()
    assert mock_handle.call_args[0][0] == "5491112345678"  # sender
    assert mock_handle.call_args[0][1] == "test message"  # text

    # Verify bot response sent
    mock_send.assert_called_once()
    assert mock_send.call_args[0][1] == "Bot response"


# ==================== LOGGING TESTS ====================

@patch('app.main.send_whatsapp_message')
def test_webhook_non_text_logs_media_type(mock_send, capsys):
    """
    Non-text message should log the media type for analytics.
    """
    payload = create_whatsapp_payload("image")

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200

    # Capture stdout and verify log
    captured = capsys.readouterr()
    assert "Non-text message" in captured.out or "[WEBHOOK]" in captured.out
    assert "type=image" in captured.out or "image" in captured.out


# ==================== EDGE CASES ====================

@patch('app.main.send_whatsapp_message')
def test_webhook_handles_missing_type_field(mock_send):
    """
    Payload without 'type' field should be treated as non-text.
    """
    payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "5491112345678"
                        # Missing "type" field
                    }]
                }
            }]
        }]
    }

    response = client.post("/webhook", json=payload)

    assert response.status_code == 200
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert "texto" in call_args[0][1].lower()
