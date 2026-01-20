"""Pydantic schemas for Guest Star endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class GuestStarSettings(TwitchBaseModel):
    """Guest star session settings."""

    is_moderator_send_live_enabled: bool
    slot_count: int
    is_browser_source_audio_enabled: bool
    group_layout: str
    browser_source_token: str | None = None


class GetGuestStarSettingsRequest(TwitchBaseModel):
    """Request params for Get Guest Star Channel Settings."""

    broadcaster_id: str
    moderator_id: str


class UpdateGuestStarSettingsRequest(TwitchBaseModel):
    """Request to update guest star settings."""

    broadcaster_id: str
    is_moderator_send_live_enabled: bool | None = None
    slot_count: int | None = Field(default=None, ge=1, le=6)
    is_browser_source_audio_enabled: bool | None = None
    group_layout: str | None = None  # TILED_LAYOUT, SCREENSHARE_LAYOUT, HORIZONTAL_LAYOUT, VERTICAL_LAYOUT


class GuestStarGuest(TwitchBaseModel):
    """Guest in a guest star session."""

    slot_id: str
    is_live: bool
    user_id: str
    user_login: str
    user_display_name: str
    volume: int
    assigned_at: datetime
    audio_settings: dict
    video_settings: dict


class GuestStarSession(TwitchBaseModel):
    """Guest star session data."""

    id: str
    guests: list[GuestStarGuest]


class GetGuestStarSessionRequest(TwitchBaseModel):
    """Request params for Get Guest Star Session."""

    broadcaster_id: str
    moderator_id: str


class CreateGuestStarSessionRequest(TwitchBaseModel):
    """Request to create a guest star session."""

    broadcaster_id: str


class EndGuestStarSessionRequest(TwitchBaseModel):
    """Request to end a guest star session."""

    broadcaster_id: str
    session_id: str


class GuestStarInvite(TwitchBaseModel):
    """Guest star invite."""

    user_id: str
    invited_at: datetime
    status: str
    is_audio_enabled: bool
    is_video_enabled: bool
    is_audio_available: bool
    is_video_available: bool


class GetGuestStarInvitesRequest(TwitchBaseModel):
    """Request params for Get Guest Star Invites."""

    broadcaster_id: str
    moderator_id: str
    session_id: str


class SendGuestStarInviteRequest(TwitchBaseModel):
    """Request to send a guest star invite."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    guest_id: str


class DeleteGuestStarInviteRequest(TwitchBaseModel):
    """Request to delete a guest star invite."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    guest_id: str


class AssignGuestStarSlotRequest(TwitchBaseModel):
    """Request to assign a guest to a slot."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    guest_id: str
    slot_id: str


class UpdateGuestStarSlotRequest(TwitchBaseModel):
    """Request to update a guest star slot."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    source_slot_id: str
    destination_slot_id: str | None = None


class DeleteGuestStarSlotRequest(TwitchBaseModel):
    """Request to remove a guest from a slot."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    guest_id: str
    slot_id: str
    should_reinvite_guest: bool | None = None


class UpdateGuestStarSlotSettingsRequest(TwitchBaseModel):
    """Request to update slot settings."""

    broadcaster_id: str
    moderator_id: str
    session_id: str
    slot_id: str
    is_audio_enabled: bool | None = None
    is_video_enabled: bool | None = None
    is_live: bool | None = None
    volume: int | None = Field(default=None, ge=0, le=100)
