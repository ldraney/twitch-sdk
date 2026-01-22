"""Pydantic schemas for Search endpoints."""

from datetime import datetime

from pydantic import Field, field_validator

from .base import TwitchBaseModel


class SearchChannel(TwitchBaseModel):
    """Channel from search results."""

    broadcaster_language: str
    broadcaster_login: str
    display_name: str
    game_id: str
    game_name: str
    id: str
    is_live: bool
    tags: list[str]
    thumbnail_url: str
    title: str
    started_at: datetime | None = None

    @field_validator("started_at", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty string to None for offline channels."""
        if v == "":
            return None
        return v


class SearchChannelsRequest(TwitchBaseModel):
    """Request params for Search Channels."""

    query: str
    live_only: bool = False
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class SearchCategory(TwitchBaseModel):
    """Category from search results."""

    id: str
    name: str
    box_art_url: str


class SearchCategoriesRequest(TwitchBaseModel):
    """Request params for Search Categories."""

    query: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None
