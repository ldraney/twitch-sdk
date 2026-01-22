"""Shared fixtures for Twitch SDK tests."""

import pytest
from datetime import datetime


@pytest.fixture
def sample_user_id() -> str:
    """Sample Twitch user ID."""
    return "123456789"


@pytest.fixture
def sample_broadcaster_id() -> str:
    """Sample broadcaster ID."""
    return "987654321"


@pytest.fixture
def sample_moderator_id() -> str:
    """Sample moderator ID."""
    return "111222333"


@pytest.fixture
def sample_stream_data() -> dict:
    """Sample stream response data."""
    return {
        "id": "40944868435",
        "user_id": "123456789",
        "user_login": "testuser",
        "user_name": "TestUser",
        "game_id": "509658",
        "game_name": "Just Chatting",
        "type": "live",
        "title": "Test Stream Title",
        "tags": ["English", "Programming"],
        "viewer_count": 1234,
        "started_at": "2024-01-15T10:00:00Z",
        "language": "en",
        "thumbnail_url": "https://example.com/thumb-{width}x{height}.jpg",
        "is_mature": False,
    }


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user response data."""
    return {
        "id": "123456789",
        "login": "testuser",
        "display_name": "TestUser",
        "type": "",
        "broadcaster_type": "affiliate",
        "description": "Test description",
        "profile_image_url": "https://example.com/profile.jpg",
        "offline_image_url": "https://example.com/offline.jpg",
        "created_at": "2020-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_banned_user_data() -> dict:
    """Sample banned user response data."""
    return {
        "user_id": "123456",
        "user_login": "banneduser",
        "user_name": "BannedUser",
        "expires_at": "2024-12-31T23:59:59Z",
        "created_at": "2024-01-01T00:00:00Z",
        "reason": "Spam",
        "moderator_id": "789012",
        "moderator_login": "moduser",
        "moderator_name": "ModUser",
    }


@pytest.fixture
def sample_poll_data() -> dict:
    """Sample poll response data."""
    return {
        "id": "poll123",
        "broadcaster_id": "987654321",
        "broadcaster_login": "broadcaster",
        "broadcaster_name": "Broadcaster",
        "title": "Test Poll",
        "choices": [
            {"id": "choice1", "title": "Option A", "votes": 10},
            {"id": "choice2", "title": "Option B", "votes": 20},
        ],
        "bits_voting_enabled": False,
        "bits_per_vote": 0,
        "channel_points_voting_enabled": True,
        "channel_points_per_vote": 100,
        "status": "ACTIVE",
        "duration": 60,
        "started_at": "2024-01-15T10:00:00Z",
    }


@pytest.fixture
def sample_prediction_data() -> dict:
    """Sample prediction response data."""
    return {
        "id": "pred123",
        "broadcaster_id": "987654321",
        "broadcaster_login": "broadcaster",
        "broadcaster_name": "Broadcaster",
        "title": "Will we win?",
        "winning_outcome_id": None,
        "outcomes": [
            {"id": "out1", "title": "Yes", "users": 50, "channel_points": 5000, "color": "BLUE"},
            {"id": "out2", "title": "No", "users": 30, "channel_points": 3000, "color": "PINK"},
        ],
        "prediction_window": 120,
        "status": "ACTIVE",
        "created_at": "2024-01-15T10:00:00Z",
    }
