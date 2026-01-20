"""Pydantic schemas for Streams endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class Stream(TwitchBaseModel):
    """Stream data from Twitch API."""

    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    game_name: str
    type: str  # "live" or ""
    title: str
    tags: list[str] = Field(default_factory=list)
    viewer_count: int
    started_at: datetime
    language: str
    thumbnail_url: str
    is_mature: bool


class GetStreamsRequest(TwitchBaseModel):
    """Request params for Get Streams endpoint."""

    user_id: list[str] | None = None
    user_login: list[str] | None = None
    game_id: list[str] | None = None
    type: str | None = None  # all, live
    language: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None


class GetFollowedStreamsRequest(TwitchBaseModel):
    """Request params for Get Followed Streams."""

    user_id: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class StreamMarker(TwitchBaseModel):
    """Stream marker data."""

    id: str
    created_at: datetime
    position_seconds: int
    description: str


class CreateStreamMarkerRequest(TwitchBaseModel):
    """Request to create a stream marker."""

    user_id: str
    description: str | None = Field(default=None, max_length=140)


class CreateStreamMarkerResponse(TwitchBaseModel):
    """Response from creating a stream marker."""

    id: str
    created_at: datetime
    position_seconds: int
    description: str


class GetStreamMarkersRequest(TwitchBaseModel):
    """Request params for Get Stream Markers."""

    user_id: str | None = None
    video_id: str | None = None
    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None


class VideoMarkers(TwitchBaseModel):
    """Markers for a video."""

    video_id: str
    markers: list[StreamMarker]


class UserMarkers(TwitchBaseModel):
    """Markers for a user's videos."""

    user_id: str
    user_login: str
    user_name: str
    videos: list[VideoMarkers]


class StreamKey(TwitchBaseModel):
    """Stream key data."""

    stream_key: str


class GetStreamKeyRequest(TwitchBaseModel):
    """Request params for Get Stream Key."""

    broadcaster_id: str
