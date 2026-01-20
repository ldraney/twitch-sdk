"""Pydantic schemas for Chat endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class Emote(TwitchBaseModel):
    """Emote data."""

    id: str
    name: str
    images: dict[str, str]
    format: list[str]
    scale: list[str]
    theme_mode: list[str]
    emote_type: str | None = None
    emote_set_id: str | None = None
    owner_id: str | None = None
    tier: str | None = None


class GetEmotesRequest(TwitchBaseModel):
    """Request params for Get Channel Emotes."""

    broadcaster_id: str


class GetEmoteSetsRequest(TwitchBaseModel):
    """Request params for Get Emote Sets."""

    emote_set_id: list[str]


class GetGlobalEmotesRequest(TwitchBaseModel):
    """Request params for Get Global Emotes (no params needed)."""

    pass


class Badge(TwitchBaseModel):
    """Chat badge data."""

    set_id: str
    versions: list[dict]


class GetBadgesRequest(TwitchBaseModel):
    """Request params for Get Channel Chat Badges."""

    broadcaster_id: str


class ChatSettings(TwitchBaseModel):
    """Chat settings data."""

    broadcaster_id: str
    emote_mode: bool
    follower_mode: bool
    follower_mode_duration: int | None = None
    moderator_id: str | None = None
    non_moderator_chat_delay: bool | None = None
    non_moderator_chat_delay_duration: int | None = None
    slow_mode: bool
    slow_mode_wait_time: int | None = None
    subscriber_mode: bool
    unique_chat_mode: bool


class GetChatSettingsRequest(TwitchBaseModel):
    """Request params for Get Chat Settings."""

    broadcaster_id: str
    moderator_id: str | None = None


class UpdateChatSettingsRequest(TwitchBaseModel):
    """Request to update chat settings."""

    broadcaster_id: str
    moderator_id: str
    emote_mode: bool | None = None
    follower_mode: bool | None = None
    follower_mode_duration: int | None = None
    non_moderator_chat_delay: bool | None = None
    non_moderator_chat_delay_duration: int | None = None
    slow_mode: bool | None = None
    slow_mode_wait_time: int | None = None
    subscriber_mode: bool | None = None
    unique_chat_mode: bool | None = None


class Chatter(TwitchBaseModel):
    """Chatter in a channel."""

    user_id: str
    user_login: str
    user_name: str


class GetChattersRequest(TwitchBaseModel):
    """Request params for Get Chatters."""

    broadcaster_id: str
    moderator_id: str
    first: int | None = Field(default=None, le=1000)
    after: str | None = None


class GetChattersResponse(TwitchBaseModel):
    """Response from Get Chatters."""

    data: list[Chatter]
    pagination: dict | None = None
    total: int


class UserChatColor(TwitchBaseModel):
    """User's chat color."""

    user_id: str
    user_login: str
    user_name: str
    color: str


class GetUserChatColorRequest(TwitchBaseModel):
    """Request params for Get User Chat Color."""

    user_id: list[str]


class UpdateUserChatColorRequest(TwitchBaseModel):
    """Request to update chat color."""

    user_id: str
    color: str  # Hex color or named color


class SendMessageRequest(TwitchBaseModel):
    """Request to send a chat message."""

    broadcaster_id: str
    sender_id: str
    message: str
    reply_parent_message_id: str | None = None


class SendMessageResponse(TwitchBaseModel):
    """Response from sending a chat message."""

    message_id: str
    is_sent: bool
    drop_reason: dict | None = None


class Announcement(TwitchBaseModel):
    """Announcement message."""

    message: str
    color: str | None = None  # blue, green, orange, purple, primary


class SendAnnouncementRequest(TwitchBaseModel):
    """Request to send an announcement."""

    broadcaster_id: str
    moderator_id: str
    message: str
    color: str | None = None


class ShoutoutRequest(TwitchBaseModel):
    """Request to send a shoutout."""

    from_broadcaster_id: str
    to_broadcaster_id: str
    moderator_id: str


class GetShoutoutsRequest(TwitchBaseModel):
    """Request params for Get Shoutouts."""

    broadcaster_id: str
    moderator_id: str
