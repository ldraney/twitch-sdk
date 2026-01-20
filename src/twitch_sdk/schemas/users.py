"""Pydantic schemas for Users endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class User(TwitchBaseModel):
    """User data from Twitch API."""

    id: str
    login: str
    display_name: str
    type: str = ""  # staff, admin, global_mod, or empty
    broadcaster_type: str = ""  # partner, affiliate, or empty
    description: str = ""
    profile_image_url: str = ""
    offline_image_url: str = ""
    email: str | None = None
    created_at: datetime


class GetUsersRequest(TwitchBaseModel):
    """Request params for Get Users endpoint."""

    id: list[str] | None = None
    login: list[str] | None = None


class UpdateUserRequest(TwitchBaseModel):
    """Request params for Update User endpoint."""

    description: str | None = None


class UserBlockTarget(TwitchBaseModel):
    """Blocked user info."""

    user_id: str
    user_login: str
    display_name: str


class GetUserBlockListRequest(TwitchBaseModel):
    """Request params for Get User Block List."""

    broadcaster_id: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class BlockUserRequest(TwitchBaseModel):
    """Request params for Block User."""

    target_user_id: str
    source_context: str | None = None  # chat, whisper
    reason: str | None = None  # harassment, spam, other


class UnblockUserRequest(TwitchBaseModel):
    """Request params for Unblock User."""

    target_user_id: str


class UserExtension(TwitchBaseModel):
    """User extension info."""

    id: str
    version: str
    name: str
    can_activate: bool
    type: list[str]


class ActiveExtension(TwitchBaseModel):
    """Active extension configuration."""

    active: bool
    id: str | None = None
    version: str | None = None
    name: str | None = None
    x: int | None = None
    y: int | None = None


class UserActiveExtensions(TwitchBaseModel):
    """User's active extensions."""

    panel: dict[str, ActiveExtension]
    overlay: dict[str, ActiveExtension]
    component: dict[str, ActiveExtension]


class UpdateUserExtensionsRequest(TwitchBaseModel):
    """Request to update active extensions."""

    data: UserActiveExtensions
