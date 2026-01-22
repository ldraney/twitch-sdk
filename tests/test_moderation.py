"""Tests for Twitch SDK moderation schemas."""

import pytest
from pydantic import ValidationError
from twitch_sdk.schemas.moderation import (
    BannedUser,
    GetBannedUsersRequest,
    BanUserRequest,
    BanUserData,
    UnbanUserRequest,
    BlockedTerm,
    GetBlockedTermsRequest,
    AddBlockedTermRequest,
    RemoveBlockedTermRequest,
    AutoModSettings,
    UpdateAutoModSettingsRequest,
    Moderator,
    GetModeratorsRequest,
    AddModeratorRequest,
    ShieldModeStatus,
    WarnUserRequest,
    DeleteChatMessagesRequest,
)


class TestBanSchemas:
    """Test ban-related schemas."""

    def test_banned_user(self, sample_banned_user_data):
        """Test BannedUser model."""
        user = BannedUser.model_validate(sample_banned_user_data)
        assert user.user_id == "123456"
        assert user.reason == "Spam"
        assert user.moderator_login == "moduser"

    def test_banned_user_no_expiry(self):
        """Test BannedUser with permanent ban (no expiry)."""
        data = {
            "user_id": "123456",
            "user_login": "banneduser",
            "user_name": "BannedUser",
            "expires_at": None,
            "created_at": "2024-01-01T00:00:00Z",
            "reason": "Permanent ban",
            "moderator_id": "789012",
            "moderator_login": "moduser",
            "moderator_name": "ModUser",
        }
        user = BannedUser.model_validate(data)
        assert user.expires_at is None

    def test_get_banned_users_request(self):
        """Test GetBannedUsersRequest model."""
        request = GetBannedUsersRequest(
            broadcaster_id="123",
            user_id=["456", "789"],
            first=50,
        )
        assert request.broadcaster_id == "123"
        assert len(request.user_id) == 2
        assert request.first == 50

    def test_get_banned_users_max_limit(self):
        """Test GetBannedUsersRequest max limit validation."""
        with pytest.raises(ValidationError):
            GetBannedUsersRequest(
                broadcaster_id="123",
                first=101,  # Exceeds le=100
            )

    def test_ban_user_request(self):
        """Test BanUserRequest model."""
        request = BanUserRequest(
            broadcaster_id="123",
            moderator_id="456",
            data=BanUserData(
                user_id="789",
                duration=3600,
                reason="Timeout for spam",
            ),
        )
        assert request.data.duration == 3600
        assert request.data.reason == "Timeout for spam"

    def test_ban_user_permanent(self):
        """Test BanUserRequest for permanent ban."""
        request = BanUserRequest(
            broadcaster_id="123",
            moderator_id="456",
            data=BanUserData(
                user_id="789",
                duration=None,  # Permanent
            ),
        )
        assert request.data.duration is None

    def test_unban_user_request(self):
        """Test UnbanUserRequest model."""
        request = UnbanUserRequest(
            broadcaster_id="123",
            moderator_id="456",
            user_id="789",
        )
        assert request.user_id == "789"


class TestBlockedTermSchemas:
    """Test blocked term schemas."""

    def test_blocked_term(self):
        """Test BlockedTerm model."""
        data = {
            "broadcaster_id": "123",
            "moderator_id": "456",
            "id": "term123",
            "text": "badword",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        }
        term = BlockedTerm.model_validate(data)
        assert term.text == "badword"

    def test_get_blocked_terms_request(self):
        """Test GetBlockedTermsRequest model."""
        request = GetBlockedTermsRequest(
            broadcaster_id="123",
            moderator_id="456",
            first=50,
        )
        assert request.first == 50

    def test_add_blocked_term_request(self):
        """Test AddBlockedTermRequest model."""
        request = AddBlockedTermRequest(
            broadcaster_id="123",
            moderator_id="456",
            text="blockedphrase",
        )
        assert request.text == "blockedphrase"

    def test_add_blocked_term_min_length(self):
        """Test AddBlockedTermRequest minimum length."""
        with pytest.raises(ValidationError):
            AddBlockedTermRequest(
                broadcaster_id="123",
                moderator_id="456",
                text="a",  # Less than min_length=2
            )

    def test_add_blocked_term_max_length(self):
        """Test AddBlockedTermRequest maximum length."""
        with pytest.raises(ValidationError):
            AddBlockedTermRequest(
                broadcaster_id="123",
                moderator_id="456",
                text="a" * 501,  # Exceeds max_length=500
            )

    def test_remove_blocked_term_request(self):
        """Test RemoveBlockedTermRequest model."""
        request = RemoveBlockedTermRequest(
            broadcaster_id="123",
            moderator_id="456",
            id="term123",
        )
        assert request.id == "term123"


class TestAutoModSchemas:
    """Test AutoMod schemas."""

    def test_automod_settings(self):
        """Test AutoModSettings model."""
        data = {
            "broadcaster_id": "123",
            "moderator_id": "456",
            "overall_level": 2,
            "disability": 2,
            "aggression": 2,
            "sexuality_sex_or_gender": 2,
            "misogyny": 2,
            "bullying": 2,
            "swearing": 2,
            "race_ethnicity_or_religion": 2,
            "sex_based_terms": 2,
        }
        settings = AutoModSettings.model_validate(data)
        assert settings.overall_level == 2

    def test_update_automod_settings_request(self):
        """Test UpdateAutoModSettingsRequest model."""
        request = UpdateAutoModSettingsRequest(
            broadcaster_id="123",
            moderator_id="456",
            overall_level=3,
        )
        assert request.overall_level == 3

    def test_update_automod_settings_level_bounds(self):
        """Test UpdateAutoModSettingsRequest level validation."""
        # Test max bound
        with pytest.raises(ValidationError):
            UpdateAutoModSettingsRequest(
                broadcaster_id="123",
                moderator_id="456",
                overall_level=5,  # Exceeds le=4
            )

        # Test min bound
        with pytest.raises(ValidationError):
            UpdateAutoModSettingsRequest(
                broadcaster_id="123",
                moderator_id="456",
                aggression=-1,  # Less than ge=0
            )


class TestModeratorSchemas:
    """Test moderator schemas."""

    def test_moderator(self):
        """Test Moderator model."""
        data = {
            "user_id": "123",
            "user_login": "moduser",
            "user_name": "ModUser",
        }
        mod = Moderator.model_validate(data)
        assert mod.user_login == "moduser"

    def test_get_moderators_request(self):
        """Test GetModeratorsRequest model."""
        request = GetModeratorsRequest(
            broadcaster_id="123",
            user_id=["456", "789"],
        )
        assert len(request.user_id) == 2

    def test_add_moderator_request(self):
        """Test AddModeratorRequest model."""
        request = AddModeratorRequest(
            broadcaster_id="123",
            user_id="456",
        )
        assert request.user_id == "456"


class TestShieldModeSchemas:
    """Test Shield Mode schemas."""

    def test_shield_mode_status(self):
        """Test ShieldModeStatus model."""
        data = {
            "is_active": True,
            "moderator_id": "456",
            "moderator_login": "moduser",
            "moderator_name": "ModUser",
            "last_activated_at": "2024-01-01T00:00:00Z",
        }
        status = ShieldModeStatus.model_validate(data)
        assert status.is_active is True


class TestWarningSchemas:
    """Test warning schemas."""

    def test_warn_user_request(self):
        """Test WarnUserRequest model."""
        request = WarnUserRequest(
            broadcaster_id="123",
            moderator_id="456",
            user_id="789",
            reason="First warning for spam",
        )
        assert request.reason == "First warning for spam"

    def test_warn_user_reason_max_length(self):
        """Test WarnUserRequest reason max length."""
        with pytest.raises(ValidationError):
            WarnUserRequest(
                broadcaster_id="123",
                moderator_id="456",
                user_id="789",
                reason="a" * 501,  # Exceeds max_length=500
            )


class TestDeleteMessagesSchemas:
    """Test delete messages schemas."""

    def test_delete_chat_messages_request(self):
        """Test DeleteChatMessagesRequest model."""
        request = DeleteChatMessagesRequest(
            broadcaster_id="123",
            moderator_id="456",
            message_id="msg789",
        )
        assert request.message_id == "msg789"

    def test_delete_chat_messages_clear_all(self):
        """Test DeleteChatMessagesRequest to clear all."""
        request = DeleteChatMessagesRequest(
            broadcaster_id="123",
            moderator_id="456",
            message_id=None,  # Clear all
        )
        assert request.message_id is None
