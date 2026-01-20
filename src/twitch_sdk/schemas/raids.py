"""Pydantic schemas for Raids endpoints."""

from datetime import datetime

from .base import TwitchBaseModel


class StartRaidRequest(TwitchBaseModel):
    """Request to start a raid."""

    from_broadcaster_id: str
    to_broadcaster_id: str


class StartRaidResponse(TwitchBaseModel):
    """Response from starting a raid."""

    created_at: datetime
    is_mature: bool


class CancelRaidRequest(TwitchBaseModel):
    """Request to cancel a raid."""

    broadcaster_id: str
