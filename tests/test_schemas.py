"""Tests for Twitch SDK schemas."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from twitch_sdk.schemas.base import TwitchResponse, Pagination
from twitch_sdk.schemas.streams import Stream, GetStreamsRequest
from twitch_sdk.schemas.chat import (
    SendMessageRequest,
    SendMessageResponse,
    SendChatMessageRequest,
    GetChattersRequest,
    Chatter,
    ChatSettings,
    SendAnnouncementRequest,
)
from twitch_sdk.schemas.polls import CreatePollRequest, PollChoiceInput, Poll, PollChoice
from twitch_sdk.schemas.predictions import (
    CreatePredictionRequest,
    PredictionOutcomeInput,
    Prediction,
    PredictionOutcome,
)


class TestBaseSchemas:
    """Test base schemas."""

    def test_pagination(self):
        """Test Pagination model."""
        data = {"cursor": "abc123"}
        pagination = Pagination.model_validate(data)
        assert pagination.cursor == "abc123"

    def test_pagination_optional(self):
        """Test Pagination with no cursor."""
        data = {}
        pagination = Pagination.model_validate(data)
        assert pagination.cursor is None

    def test_twitch_response(self):
        """Test TwitchResponse model."""
        data = {
            "data": [{"id": "1", "name": "test"}],
            "pagination": {"cursor": "next"},
        }
        response = TwitchResponse[dict].model_validate(data)
        assert len(response.data) == 1
        assert response.pagination.cursor == "next"

    def test_twitch_response_empty_data(self):
        """Test TwitchResponse with empty data."""
        data = {"data": []}
        response = TwitchResponse[dict].model_validate(data)
        assert len(response.data) == 0


class TestStreamSchemas:
    """Test stream schemas."""

    def test_stream_model(self, sample_stream_data):
        """Test Stream model."""
        stream = Stream.model_validate(sample_stream_data)
        assert stream.id == "40944868435"
        assert stream.user_name == "TestUser"
        assert stream.viewer_count == 1234
        assert stream.game_name == "Just Chatting"

    def test_get_streams_request_user_login(self):
        """Test GetStreamsRequest with user_login."""
        request = GetStreamsRequest(
            user_login=["test1", "test2"],
            first=10,
        )
        assert request.user_login == ["test1", "test2"]
        assert request.first == 10

    def test_get_streams_request_game_id(self):
        """Test GetStreamsRequest with game_id."""
        request = GetStreamsRequest(game_id=["509658", "123456"])
        assert request.game_id == ["509658", "123456"]

    def test_get_streams_request_language(self):
        """Test GetStreamsRequest with language filter."""
        request = GetStreamsRequest(language=["en", "es"])
        assert request.language == ["en", "es"]


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

    def test_send_chat_message_request_alias(self):
        """Test SendChatMessageRequest alias works."""
        request = SendChatMessageRequest(
            broadcaster_id="123",
            sender_id="456",
            message="Test message",
        )
        assert request.broadcaster_id == "123"
        assert isinstance(request, SendMessageRequest)

    def test_send_message_with_reply(self):
        """Test SendMessageRequest with reply."""
        request = SendMessageRequest(
            broadcaster_id="123",
            sender_id="456",
            message="Reply to this!",
            reply_parent_message_id="msg789",
        )
        assert request.reply_parent_message_id == "msg789"

    def test_send_message_response(self):
        """Test SendMessageResponse model."""
        data = {
            "message_id": "abc123",
            "is_sent": True,
        }
        response = SendMessageResponse.model_validate(data)
        assert response.is_sent is True
        assert response.message_id == "abc123"

    def test_send_message_response_with_drop(self):
        """Test SendMessageResponse with drop reason."""
        data = {
            "message_id": "abc123",
            "is_sent": False,
            "drop_reason": {"code": "msg_duplicate", "message": "Duplicate message"},
        }
        response = SendMessageResponse.model_validate(data)
        assert response.is_sent is False
        assert response.drop_reason["code"] == "msg_duplicate"

    def test_get_chatters_request(self):
        """Test GetChattersRequest model."""
        request = GetChattersRequest(
            broadcaster_id="123",
            moderator_id="456",
            first=100,
        )
        assert request.broadcaster_id == "123"
        assert request.first == 100

    def test_get_chatters_request_max_limit(self):
        """Test GetChattersRequest respects max limit."""
        with pytest.raises(ValidationError):
            GetChattersRequest(
                broadcaster_id="123",
                moderator_id="456",
                first=1001,  # Exceeds le=1000
            )

    def test_chatter_model(self):
        """Test Chatter model."""
        data = {
            "user_id": "123",
            "user_login": "testuser",
            "user_name": "TestUser",
        }
        chatter = Chatter.model_validate(data)
        assert chatter.user_id == "123"
        assert chatter.user_name == "TestUser"

    def test_chat_settings(self):
        """Test ChatSettings model."""
        data = {
            "broadcaster_id": "123",
            "emote_mode": False,
            "follower_mode": True,
            "follower_mode_duration": 10,
            "slow_mode": True,
            "slow_mode_wait_time": 30,
            "subscriber_mode": False,
            "unique_chat_mode": False,
        }
        settings = ChatSettings.model_validate(data)
        assert settings.follower_mode is True
        assert settings.slow_mode_wait_time == 30

    def test_send_announcement_request(self):
        """Test SendAnnouncementRequest model."""
        request = SendAnnouncementRequest(
            broadcaster_id="123",
            moderator_id="456",
            message="Important announcement!",
            color="blue",
        )
        assert request.color == "blue"


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
        with pytest.raises(ValidationError):
            CreatePollRequest(
                broadcaster_id="123",
                title="Test Poll",
                choices=[PollChoiceInput(title="Only One")],
                duration=60,
            )

    def test_poll_validation_max_choices(self):
        """Test that poll allows max 5 choices."""
        with pytest.raises(ValidationError):
            CreatePollRequest(
                broadcaster_id="123",
                title="Test Poll",
                choices=[PollChoiceInput(title=f"Option {i}") for i in range(6)],
                duration=60,
            )

    def test_poll_validation_duration_min(self):
        """Test poll minimum duration."""
        with pytest.raises(ValidationError):
            CreatePollRequest(
                broadcaster_id="123",
                title="Test Poll",
                choices=[
                    PollChoiceInput(title="A"),
                    PollChoiceInput(title="B"),
                ],
                duration=10,  # Less than ge=15
            )

    def test_poll_validation_duration_max(self):
        """Test poll maximum duration."""
        with pytest.raises(ValidationError):
            CreatePollRequest(
                broadcaster_id="123",
                title="Test Poll",
                choices=[
                    PollChoiceInput(title="A"),
                    PollChoiceInput(title="B"),
                ],
                duration=2000,  # More than le=1800
            )

    def test_poll_validation_title_max_length(self):
        """Test poll title max length."""
        with pytest.raises(ValidationError):
            CreatePollRequest(
                broadcaster_id="123",
                title="A" * 61,  # Exceeds max_length=60
                choices=[
                    PollChoiceInput(title="A"),
                    PollChoiceInput(title="B"),
                ],
                duration=60,
            )

    def test_poll_choice_input_max_length(self):
        """Test poll choice title max length."""
        with pytest.raises(ValidationError):
            PollChoiceInput(title="A" * 26)  # Exceeds max_length=25

    def test_poll_response_parsing(self, sample_poll_data):
        """Test Poll response model."""
        poll = Poll.model_validate(sample_poll_data)
        assert poll.id == "poll123"
        assert poll.status == "ACTIVE"
        assert len(poll.choices) == 2

    def test_poll_choice_optional_id(self):
        """Test PollChoice with optional id field."""
        # This tests the fix for the SDK bug where id was required
        data = {"title": "Option A", "votes": 0}
        choice = PollChoice.model_validate(data)
        assert choice.id is None
        assert choice.title == "Option A"


class TestPredictionSchemas:
    """Test prediction schemas."""

    def test_create_prediction_request(self):
        """Test CreatePredictionRequest model."""
        request = CreatePredictionRequest(
            broadcaster_id="123",
            title="Will we win?",
            outcomes=[
                PredictionOutcomeInput(title="Yes"),
                PredictionOutcomeInput(title="No"),
            ],
            prediction_window=120,
        )
        assert request.title == "Will we win?"
        assert len(request.outcomes) == 2

    def test_prediction_validation_min_outcomes(self):
        """Test prediction requires at least 2 outcomes."""
        with pytest.raises(ValidationError):
            CreatePredictionRequest(
                broadcaster_id="123",
                title="Test",
                outcomes=[PredictionOutcomeInput(title="Only One")],
                prediction_window=120,
            )

    def test_prediction_validation_max_outcomes(self):
        """Test prediction allows max 10 outcomes."""
        with pytest.raises(ValidationError):
            CreatePredictionRequest(
                broadcaster_id="123",
                title="Test",
                outcomes=[PredictionOutcomeInput(title=f"Opt{i}") for i in range(11)],
                prediction_window=120,
            )

    def test_prediction_validation_window_min(self):
        """Test prediction minimum window."""
        with pytest.raises(ValidationError):
            CreatePredictionRequest(
                broadcaster_id="123",
                title="Test",
                outcomes=[
                    PredictionOutcomeInput(title="Yes"),
                    PredictionOutcomeInput(title="No"),
                ],
                prediction_window=20,  # Less than ge=30
            )

    def test_prediction_response_parsing(self, sample_prediction_data):
        """Test Prediction response model."""
        pred = Prediction.model_validate(sample_prediction_data)
        assert pred.id == "pred123"
        assert pred.status == "ACTIVE"
        assert len(pred.outcomes) == 2

    def test_prediction_outcome_optional_fields(self):
        """Test PredictionOutcome with optional id and color."""
        # This tests the fix for the SDK bug
        data = {"title": "Yes", "users": 0, "channel_points": 0}
        outcome = PredictionOutcome.model_validate(data)
        assert outcome.id is None
        assert outcome.color is None
        assert outcome.title == "Yes"
