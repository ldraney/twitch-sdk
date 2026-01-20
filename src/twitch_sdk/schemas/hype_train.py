"""Pydantic schemas for Hype Train endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class HypeTrainContribution(TwitchBaseModel):
    """Hype train contribution."""

    total: int
    type: str  # BITS, SUBS, OTHER
    user: str


class HypeTrainEvent(TwitchBaseModel):
    """Hype train event data."""

    id: str
    event_type: str
    event_timestamp: datetime
    version: str
    event_data: dict


class HypeTrain(TwitchBaseModel):
    """Hype train data."""

    id: str
    broadcaster_id: str
    started_at: datetime
    expires_at: datetime
    cooldown_end_time: datetime
    level: int
    goal: int
    total: int
    top_contributions: list[HypeTrainContribution]
    last_contribution: HypeTrainContribution


class GetHypeTrainEventsRequest(TwitchBaseModel):
    """Request params for Get Hype Train Events."""

    broadcaster_id: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None
