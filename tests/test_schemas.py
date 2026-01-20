"""Tests for Twitch SDK schemas."""

import pytest
from datetime import datetime
from twitch_sdk.schemas.base import TwitchResponse, Pagination
from twitch_sdk.schemas.streams import Stream, GetStreamsRequest
from twitch_sdk.schemas.chat import SendMessageRequest, SendMessageResponse
from twitch_sdk.schemas.polls import CreatePollRequest, PollChoiceInput


class TestBaseSchemas:
    """Test base schemas."""

    def test_pagination(self):
        """Test Pagination model."""
        data = {"cursor": "abc123"}
        pagination = Pagination.model_validate(data)
        assert pagination.cursor == "abc123"

    def test_twitch_response(self):
        """Test TwitchResponse model."""
        data = {
            "data": [{"id": "1", "name": "test"}],
            "pagination": {"cursor": "next"},
        }
        response = TwitchResponse[dict].model_validate(data)
        assert len(response.data) == 1
        assert response.pagination.cursor == "next"


class TestStreamSchemas:
    """Test stream schemas."""

    def test_stream_model(self):
        """Test Stream model."""
        data = {
            "id": "123",
            "user_id": "456",
            "user_login": "testuser",
            "user_name": "TestUser",
            "game_id": "789",
            "game_name": "Test Game",
            "type": "live",
            "title": "Test Stream",
            "tags": ["tag1", "tag2"],
            "viewer_count": 100,
            "started_at": "2024-01-01T00:00:00Z",
            "language": "en",
            "thumbnail_url": "https://example.com/thumb.jpg",
            "is_mature": False,
        }
        stream = Stream.model_validate(data)
        assert stream.id == "123"
        assert stream.user_name == "TestUser"
        assert stream.viewer_count == 100

    def test_get_streams_request(self):
        """Test GetStreamsRequest model."""
        request = GetStreamsRequest(
            user_login=["test1", "test2"],
            first=10,
        )
        assert request.user_login == ["test1", "test2"]
        assert request.first == 10


class TestChatSchemas:
    """Test chat schemas."""

    def test_send_message_request(self):
        """Test SendMessageRequest model."""
        request = SendMessageRequest(
            broadcaster_id="123",
            sender_id="456",
            message="Hello world!",
        )
        assert request.broadcaster_id == "123"
        assert request.message == "Hello world!"

    def test_send_message_response(self):
        """Test SendMessageResponse model."""
        data = {
            "message_id": "abc123",
            "is_sent": True,
        }
        response = SendMessageResponse.model_validate(data)
        assert response.is_sent is True


class TestPollSchemas:
    """Test poll schemas."""

    def test_create_poll_request(self):
        """Test CreatePollRequest model."""
        request = CreatePollRequest(
            broadcaster_id="123",
            title="Test Poll",
            choices=[
                PollChoiceInput(title="Option A"),
                PollChoiceInput(title="Option B"),
            ],
            duration=60,
        )
        assert request.title == "Test Poll"
        assert len(request.choices) == 2

    def test_poll_validation_min_choices(self):
        """Test that poll requires at least 2 choices."""
        with pytest.raises(Exception):
            CreatePollRequest(
                broadcaster_id="123",
                title="Test Poll",
                choices=[PollChoiceInput(title="Only One")],
                duration=60,
            )
