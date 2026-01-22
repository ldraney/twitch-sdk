"""Tests for Twitch SDK user schemas."""

import pytest
from pydantic import ValidationError
from twitch_sdk.schemas.users import (
    User,
    GetUsersRequest,
    UpdateUserRequest,
    UserBlockTarget,
    GetUserBlockListRequest,
    BlockUserRequest,
    UnblockUserRequest,
)


class TestUserSchemas:
    """Test user schemas."""

    def test_user_model(self, sample_user_data):
        """Test User model."""
        user = User.model_validate(sample_user_data)
        assert user.id == "123456789"
        assert user.login == "testuser"
        assert user.display_name == "TestUser"
        assert user.broadcaster_type == "affiliate"

    def test_user_model_minimal(self):
        """Test User model with minimal data."""
        data = {
            "id": "123",
            "login": "testuser",
            "display_name": "TestUser",
            "created_at": "2020-01-01T00:00:00Z",
        }
        user = User.model_validate(data)
        assert user.type == ""
        assert user.broadcaster_type == ""
        assert user.description == ""

    def test_user_with_email(self):
        """Test User model with email (requires user:read:email scope)."""
        data = {
            "id": "123",
            "login": "testuser",
            "display_name": "TestUser",
            "email": "test@example.com",
            "created_at": "2020-01-01T00:00:00Z",
        }
        user = User.model_validate(data)
        assert user.email == "test@example.com"

    def test_user_staff_type(self):
        """Test User model with staff type."""
        data = {
            "id": "123",
            "login": "staffuser",
            "display_name": "StaffUser",
            "type": "staff",
            "created_at": "2020-01-01T00:00:00Z",
        }
        user = User.model_validate(data)
        assert user.type == "staff"

    def test_get_users_request_by_id(self):
        """Test GetUsersRequest by user IDs."""
        request = GetUsersRequest(
            id=["123", "456", "789"],
        )
        assert len(request.id) == 3

    def test_get_users_request_by_login(self):
        """Test GetUsersRequest by user logins."""
        request = GetUsersRequest(
            login=["user1", "user2"],
        )
        assert len(request.login) == 2

    def test_get_users_request_mixed(self):
        """Test GetUsersRequest with both id and login."""
        request = GetUsersRequest(
            id=["123"],
            login=["user1"],
        )
        assert request.id == ["123"]
        assert request.login == ["user1"]

    def test_get_users_request_empty(self):
        """Test GetUsersRequest with no params (returns authenticated user)."""
        request = GetUsersRequest()
        assert request.id is None
        assert request.login is None

    def test_update_user_request(self):
        """Test UpdateUserRequest model."""
        request = UpdateUserRequest(
            description="New channel description",
        )
        assert request.description == "New channel description"

    def test_update_user_request_empty(self):
        """Test UpdateUserRequest with no changes."""
        request = UpdateUserRequest()
        assert request.description is None


class TestUserBlockSchemas:
    """Test user block schemas."""

    def test_user_block_target(self):
        """Test UserBlockTarget model."""
        data = {
            "user_id": "123",
            "user_login": "blockeduser",
            "display_name": "BlockedUser",
        }
        target = UserBlockTarget.model_validate(data)
        assert target.user_id == "123"
        assert target.display_name == "BlockedUser"

    def test_get_user_block_list_request(self):
        """Test GetUserBlockListRequest model."""
        request = GetUserBlockListRequest(
            broadcaster_id="123",
            first=50,
        )
        assert request.first == 50

    def test_get_user_block_list_max_first(self):
        """Test GetUserBlockListRequest max first validation."""
        with pytest.raises(ValidationError):
            GetUserBlockListRequest(
                broadcaster_id="123",
                first=101,  # Exceeds le=100
            )

    def test_block_user_request(self):
        """Test BlockUserRequest model."""
        request = BlockUserRequest(
            target_user_id="456",
            source_context="chat",
            reason="harassment",
        )
        assert request.target_user_id == "456"
        assert request.source_context == "chat"
        assert request.reason == "harassment"

    def test_block_user_request_minimal(self):
        """Test BlockUserRequest with only required fields."""
        request = BlockUserRequest(target_user_id="456")
        assert request.source_context is None
        assert request.reason is None

    def test_unblock_user_request(self):
        """Test UnblockUserRequest model."""
        request = UnblockUserRequest(target_user_id="456")
        assert request.target_user_id == "456"


class TestModelSerialization:
    """Test model serialization for API requests."""

    def test_get_users_request_dump(self):
        """Test GetUsersRequest serialization."""
        request = GetUsersRequest(id=["123", "456"])
        dumped = request.model_dump(exclude_none=True)
        assert dumped == {"id": ["123", "456"]}

    def test_get_users_request_dump_excludes_none(self):
        """Test GetUsersRequest excludes None values."""
        request = GetUsersRequest(id=["123"])
        dumped = request.model_dump(exclude_none=True)
        assert "login" not in dumped

    def test_block_user_request_dump(self):
        """Test BlockUserRequest serialization."""
        request = BlockUserRequest(
            target_user_id="456",
            source_context="chat",
        )
        dumped = request.model_dump(exclude_none=True)
        assert dumped == {
            "target_user_id": "456",
            "source_context": "chat",
        }
        assert "reason" not in dumped
