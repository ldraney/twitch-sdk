"""Pydantic schemas for Ads endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class StartCommercialRequest(TwitchBaseModel):
    """Request to start a commercial."""

    broadcaster_id: str
    length: int  # 30, 60, 90, 120, 150, 180


class StartCommercialResponse(TwitchBaseModel):
    """Response from starting a commercial."""

    length: int
    message: str
    retry_after: int


class AdSchedule(TwitchBaseModel):
    """Ad schedule information."""

    snooze_count: int
    snooze_refresh_at: datetime | None = None
    next_ad_at: datetime | None = None
    duration: int
    last_ad_at: datetime | None = None
    preroll_free_time: int


class GetAdScheduleRequest(TwitchBaseModel):
    """Request params for Get Ad Schedule."""

    broadcaster_id: str


class SnoozeNextAdRequest(TwitchBaseModel):
    """Request to snooze the next ad."""

    broadcaster_id: str


class SnoozeNextAdResponse(TwitchBaseModel):
    """Response from snoozing an ad."""

    snooze_count: int
    snooze_refresh_at: datetime | None = None
    next_ad_at: datetime | None = None
