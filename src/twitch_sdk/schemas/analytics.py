"""Pydantic schemas for Analytics endpoints."""

from datetime import datetime

from pydantic import Field

from .base import DateRange, TwitchBaseModel


class ExtensionAnalytics(TwitchBaseModel):
    """Extension analytics data."""

    extension_id: str
    URL: str
    type: str
    date_range: DateRange


class GetExtensionAnalyticsRequest(TwitchBaseModel):
    """Request params for Get Extension Analytics."""

    extension_id: str | None = None
    type: str | None = None  # overview_v2
    started_at: datetime | None = None
    ended_at: datetime | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class GameAnalytics(TwitchBaseModel):
    """Game analytics data."""

    game_id: str
    URL: str
    type: str
    date_range: DateRange


class GetGameAnalyticsRequest(TwitchBaseModel):
    """Request params for Get Game Analytics."""

    game_id: str | None = None
    type: str | None = None  # overview_v2
    started_at: datetime | None = None
    ended_at: datetime | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None
