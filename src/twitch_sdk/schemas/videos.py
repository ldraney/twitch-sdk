"""Pydantic schemas for Videos endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class MutedSegment(TwitchBaseModel):
    """Muted segment in a video."""

    duration: int
    offset: int


class Video(TwitchBaseModel):
    """Video data from Twitch API."""

    id: str
    stream_id: str | None = None
    user_id: str
    user_login: str
    user_name: str
    title: str
    description: str
    created_at: datetime
    published_at: datetime
    url: str
    thumbnail_url: str
    viewable: str
    view_count: int
    language: str
    type: str  # archive, highlight, upload
    duration: str
    muted_segments: list[MutedSegment] | None = None


class GetVideosRequest(TwitchBaseModel):
    """Request params for Get Videos."""

    id: list[str] | None = None
    user_id: str | None = None
    game_id: str | None = None
    language: str | None = None
    period: str | None = None  # all, day, week, month
    sort: str | None = None  # time, trending, views
    type: str | None = None  # all, archive, highlight, upload
    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None


class DeleteVideosRequest(TwitchBaseModel):
    """Request to delete videos."""

    id: list[str] = Field(max_length=5)
