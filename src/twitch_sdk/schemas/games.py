"""Pydantic schemas for Games endpoints."""

from pydantic import Field

from .base import TwitchBaseModel


class Game(TwitchBaseModel):
    """Game/category data."""

    id: str
    name: str
    box_art_url: str
    igdb_id: str | None = None


class GetGamesRequest(TwitchBaseModel):
    """Request params for Get Games."""

    id: list[str] | None = None
    name: list[str] | None = None
    igdb_id: list[str] | None = None


class GetTopGamesRequest(TwitchBaseModel):
    """Request params for Get Top Games."""

    first: int | None = Field(default=None, le=100)
    before: str | None = None
    after: str | None = None
