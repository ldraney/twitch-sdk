"""Pydantic schemas for Teams endpoints."""

from datetime import datetime

from .base import TwitchBaseModel


class TeamMember(TwitchBaseModel):
    """Team member info."""

    user_id: str
    user_login: str
    user_name: str


class Team(TwitchBaseModel):
    """Team data."""

    id: str
    team_name: str
    team_display_name: str
    info: str
    thumbnail_url: str
    banner: str | None = None
    background_image_url: str | None = None
    created_at: datetime
    updated_at: datetime
    users: list[TeamMember] | None = None


class GetTeamsRequest(TwitchBaseModel):
    """Request params for Get Teams."""

    name: str | None = None
    id: str | None = None


class GetChannelTeamsRequest(TwitchBaseModel):
    """Request params for Get Channel Teams."""

    broadcaster_id: str
