"""Pydantic schemas for Moderation endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class BannedUser(TwitchBaseModel):
    """Banned user data."""

    user_id: str
    user_login: str
    user_name: str
    expires_at: datetime | None = None
    created_at: datetime
    reason: str
    moderator_id: str
    moderator_login: str
    moderator_name: str


class GetBannedUsersRequest(TwitchBaseModel):
    """Request params for Get Banned Users."""

    broadcaster_id: str
    user_id: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None


class BanUserRequest(TwitchBaseModel):
    """Request to ban a user."""

    broadcaster_id: str
    moderator_id: str
    data: "BanUserData"


class BanUserData(TwitchBaseModel):
    """Ban user data payload."""

    user_id: str
    duration: int | None = None  # Seconds, None for permanent
    reason: str | None = None


class BanUserResponse(TwitchBaseModel):
    """Response from banning a user."""

    broadcaster_id: str
    moderator_id: str
    user_id: str
    created_at: datetime
    end_time: datetime | None = None


class UnbanUserRequest(TwitchBaseModel):
    """Request to unban a user."""

    broadcaster_id: str
    moderator_id: str
    user_id: str


class UnbanRequest(TwitchBaseModel):
    """Unban request data."""

    id: str
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    moderator_id: str
    moderator_login: str
    moderator_name: str
    user_id: str
    user_login: str
    user_name: str
    text: str
    status: str
    created_at: datetime
    resolved_at: datetime | None = None
    resolution_text: str | None = None


class GetUnbanRequestsRequest(TwitchBaseModel):
    """Request params for Get Unban Requests."""

    broadcaster_id: str
    moderator_id: str
    status: str | None = None  # pending, approved, denied, acknowledged, canceled
    user_id: str | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class ResolveUnbanRequestRequest(TwitchBaseModel):
    """Request to resolve an unban request."""

    broadcaster_id: str
    moderator_id: str
    unban_request_id: str
    status: str  # approved, denied
    resolution_text: str | None = None


class BlockedTerm(TwitchBaseModel):
    """Blocked term data."""

    broadcaster_id: str
    moderator_id: str
    id: str
    text: str
    created_at: datetime
    updated_at: datetime
    expires_at: datetime | None = None


class GetBlockedTermsRequest(TwitchBaseModel):
    """Request params for Get Blocked Terms."""

    broadcaster_id: str
    moderator_id: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class AddBlockedTermRequest(TwitchBaseModel):
    """Request to add a blocked term."""

    broadcaster_id: str
    moderator_id: str
    text: str = Field(min_length=2, max_length=500)


class RemoveBlockedTermRequest(TwitchBaseModel):
    """Request to remove a blocked term."""

    broadcaster_id: str
    moderator_id: str
    id: str


class AutoModSettings(TwitchBaseModel):
    """AutoMod settings data."""

    broadcaster_id: str
    moderator_id: str
    overall_level: int | None = None
    disability: int
    aggression: int
    sexuality_sex_or_gender: int
    misogyny: int
    bullying: int
    swearing: int
    race_ethnicity_or_religion: int
    sex_based_terms: int


class GetAutoModSettingsRequest(TwitchBaseModel):
    """Request params for Get AutoMod Settings."""

    broadcaster_id: str
    moderator_id: str


class UpdateAutoModSettingsRequest(TwitchBaseModel):
    """Request to update AutoMod settings."""

    broadcaster_id: str
    moderator_id: str
    overall_level: int | None = Field(default=None, ge=0, le=4)
    aggression: int | None = Field(default=None, ge=0, le=4)
    bullying: int | None = Field(default=None, ge=0, le=4)
    disability: int | None = Field(default=None, ge=0, le=4)
    misogyny: int | None = Field(default=None, ge=0, le=4)
    race_ethnicity_or_religion: int | None = Field(default=None, ge=0, le=4)
    sex_based_terms: int | None = Field(default=None, ge=0, le=4)
    sexuality_sex_or_gender: int | None = Field(default=None, ge=0, le=4)
    swearing: int | None = Field(default=None, ge=0, le=4)


class Moderator(TwitchBaseModel):
    """Moderator data."""

    user_id: str
    user_login: str
    user_name: str


class GetModeratorsRequest(TwitchBaseModel):
    """Request params for Get Moderators."""

    broadcaster_id: str
    user_id: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class AddModeratorRequest(TwitchBaseModel):
    """Request to add a moderator."""

    broadcaster_id: str
    user_id: str


class RemoveModeratorRequest(TwitchBaseModel):
    """Request to remove a moderator."""

    broadcaster_id: str
    user_id: str


class ShieldModeStatus(TwitchBaseModel):
    """Shield mode status."""

    is_active: bool
    moderator_id: str
    moderator_login: str
    moderator_name: str
    last_activated_at: datetime


class GetShieldModeStatusRequest(TwitchBaseModel):
    """Request params for Get Shield Mode Status."""

    broadcaster_id: str
    moderator_id: str


class UpdateShieldModeStatusRequest(TwitchBaseModel):
    """Request to update shield mode status."""

    broadcaster_id: str
    moderator_id: str
    is_active: bool


class WarnUserRequest(TwitchBaseModel):
    """Request to warn a user."""

    broadcaster_id: str
    moderator_id: str
    user_id: str
    reason: str = Field(max_length=500)


class DeleteChatMessagesRequest(TwitchBaseModel):
    """Request to delete chat messages."""

    broadcaster_id: str
    moderator_id: str
    message_id: str | None = None  # If None, clears all messages


class ManageHeldAutoModMessageRequest(TwitchBaseModel):
    """Request to manage a held AutoMod message."""

    user_id: str
    msg_id: str
    action: str  # ALLOW, DENY
