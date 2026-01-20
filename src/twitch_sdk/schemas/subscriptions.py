"""Pydantic schemas for Subscriptions endpoints."""

from pydantic import Field

from .base import TwitchBaseModel


class Subscription(TwitchBaseModel):
    """Subscription data."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    gifter_id: str | None = None
    gifter_login: str | None = None
    gifter_name: str | None = None
    is_gift: bool
    plan_name: str
    tier: str  # 1000, 2000, 3000
    user_id: str
    user_login: str
    user_name: str


class GetBroadcasterSubscriptionsRequest(TwitchBaseModel):
    """Request params for Get Broadcaster Subscriptions."""

    broadcaster_id: str
    user_id: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class GetBroadcasterSubscriptionsResponse(TwitchBaseModel):
    """Response from Get Broadcaster Subscriptions."""

    data: list[Subscription]
    pagination: dict | None = None
    total: int
    points: int


class UserSubscription(TwitchBaseModel):
    """User's subscription to a broadcaster."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    gifter_id: str | None = None
    gifter_login: str | None = None
    gifter_name: str | None = None
    is_gift: bool
    tier: str


class CheckUserSubscriptionRequest(TwitchBaseModel):
    """Request params for Check User Subscription."""

    broadcaster_id: str
    user_id: str
