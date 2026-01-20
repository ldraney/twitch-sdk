"""Pydantic schemas for Goals endpoints."""

from datetime import datetime

from .base import TwitchBaseModel


class Goal(TwitchBaseModel):
    """Creator goal data."""

    id: str
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    type: str  # follower, subscription, subscription_count, new_subscription, new_subscription_count
    description: str
    current_amount: int
    target_amount: int
    created_at: datetime


class GetGoalsRequest(TwitchBaseModel):
    """Request params for Get Creator Goals."""

    broadcaster_id: str
