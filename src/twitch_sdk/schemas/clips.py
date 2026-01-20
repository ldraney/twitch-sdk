"""Pydantic schemas for Clips endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class Clip(TwitchBaseModel):
    """Clip data from Twitch API."""

    id: str
    url: str
    embed_url: str
    broadcaster_id: str
    broadcaster_name: str
    creator_id: str
    creator_name: str
    video_id: str
    game_id: str
    language: str
    title: str
    view_count: int
    created_at: datetime
    thumbnail_url: str
    duration: float
    vod_offset: int | None = None
    is_featured: bool


class CreateClipRequest(TwitchBaseModel):
    """Request to create a clip."""

    broadcaster_id: str
    has_delay: bool = False


class CreateClipResponse(TwitchBaseModel):
    """Response from creating a clip."""

    id: str
    edit_url: str


class GetClipsRequest(TwitchBaseModel):
    """Request params for Get Clips."""

    broadcaster_id: str | None = None
    game_id: str | None = None
    id: list[str] | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None
    is_featured: bool | None = None
