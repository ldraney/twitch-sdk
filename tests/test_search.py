"""Tests for Twitch SDK search schemas."""

import pytest
from pydantic import ValidationError
from twitch_sdk.schemas.search import (
    SearchChannel,
    SearchChannelsRequest,
    SearchCategory,
    SearchCategoriesRequest,
)


class TestSearchChannelSchemas:
    """Test search channel schemas."""

    def test_search_channel(self):
        """Test SearchChannel model with live channel."""
        data = {
            "broadcaster_language": "en",
            "broadcaster_login": "testuser",
            "display_name": "TestUser",
            "game_id": "509658",
            "game_name": "Just Chatting",
            "id": "123456",
            "is_live": True,
            "tags": ["English", "Programming"],
            "thumbnail_url": "https://example.com/thumb.jpg",
            "title": "Live stream!",
            "started_at": "2024-01-15T10:00:00Z",
        }
        channel = SearchChannel.model_validate(data)
        assert channel.is_live is True
        assert channel.started_at is not None
        assert channel.display_name == "TestUser"

    def test_search_channel_offline(self):
        """Test SearchChannel model with offline channel."""
        data = {
            "broadcaster_language": "en",
            "broadcaster_login": "testuser",
            "display_name": "TestUser",
            "game_id": "509658",
            "game_name": "Just Chatting",
            "id": "123456",
            "is_live": False,
            "tags": ["English"],
            "thumbnail_url": "https://example.com/thumb.jpg",
            "title": "Offline",
            "started_at": None,
        }
        channel = SearchChannel.model_validate(data)
        assert channel.is_live is False
        assert channel.started_at is None

    def test_search_channel_empty_started_at_validator(self):
        """Test SearchChannel handles empty string for started_at.

        This tests the SDK bug fix where Twitch API returns empty string
        for offline channels instead of null.
        """
        data = {
            "broadcaster_language": "en",
            "broadcaster_login": "testuser",
            "display_name": "TestUser",
            "game_id": "509658",
            "game_name": "Just Chatting",
            "id": "123456",
            "is_live": False,
            "tags": [],
            "thumbnail_url": "https://example.com/thumb.jpg",
            "title": "Offline",
            "started_at": "",  # Empty string from Twitch API
        }
        channel = SearchChannel.model_validate(data)
        assert channel.started_at is None

    def test_search_channels_request(self):
        """Test SearchChannelsRequest model."""
        request = SearchChannelsRequest(
            query="fortnite",
            live_only=True,
            first=25,
        )
        assert request.query == "fortnite"
        assert request.live_only is True
        assert request.first == 25

    def test_search_channels_request_defaults(self):
        """Test SearchChannelsRequest default values."""
        request = SearchChannelsRequest(query="minecraft")
        assert request.live_only is False
        assert request.first is None

    def test_search_channels_max_first(self):
        """Test SearchChannelsRequest max first validation."""
        with pytest.raises(ValidationError):
            SearchChannelsRequest(
                query="test",
                first=101,  # Exceeds le=100
            )


class TestSearchCategorySchemas:
    """Test search category schemas."""

    def test_search_category(self):
        """Test SearchCategory model."""
        data = {
            "id": "509658",
            "name": "Just Chatting",
            "box_art_url": "https://example.com/boxart.jpg",
        }
        category = SearchCategory.model_validate(data)
        assert category.id == "509658"
        assert category.name == "Just Chatting"

    def test_search_categories_request(self):
        """Test SearchCategoriesRequest model."""
        request = SearchCategoriesRequest(
            query="minecraft",
            first=10,
        )
        assert request.query == "minecraft"
        assert request.first == 10

    def test_search_categories_max_first(self):
        """Test SearchCategoriesRequest max first validation."""
        with pytest.raises(ValidationError):
            SearchCategoriesRequest(
                query="test",
                first=101,  # Exceeds le=100
            )

    def test_search_categories_with_pagination(self):
        """Test SearchCategoriesRequest with pagination cursor."""
        request = SearchCategoriesRequest(
            query="game",
            after="cursor123",
        )
        assert request.after == "cursor123"
