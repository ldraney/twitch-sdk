"""Pydantic schemas for EventSub endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class EventSubTransport(TwitchBaseModel):
    """EventSub transport configuration."""

    method: str  # webhook, websocket, conduit
    callback: str | None = None
    secret: str | None = None
    session_id: str | None = None
    conduit_id: str | None = None
    connected_at: datetime | None = None
    disconnected_at: datetime | None = None


class EventSubSubscription(TwitchBaseModel):
    """EventSub subscription data."""

    id: str
    status: str  # enabled, webhook_callback_verification_pending, etc.
    type: str
    version: str
    condition: dict
    created_at: datetime
    transport: EventSubTransport
    cost: int


class CreateEventSubSubscriptionRequest(TwitchBaseModel):
    """Request to create an EventSub subscription."""

    type: str
    version: str
    condition: dict
    transport: dict


class GetEventSubSubscriptionsRequest(TwitchBaseModel):
    """Request params for Get EventSub Subscriptions."""

    status: str | None = None
    type: str | None = None
    user_id: str | None = None
    after: str | None = None


class GetEventSubSubscriptionsResponse(TwitchBaseModel):
    """Response from Get EventSub Subscriptions."""

    data: list[EventSubSubscription]
    total: int
    total_cost: int
    max_total_cost: int
    pagination: dict | None = None


class DeleteEventSubSubscriptionRequest(TwitchBaseModel):
    """Request to delete an EventSub subscription."""

    id: str


# WebSocket message types
class WebSocketWelcome(TwitchBaseModel):
    """WebSocket welcome message."""

    session_id: str
    status: str
    connected_at: datetime
    keepalive_timeout_seconds: int
    reconnect_url: str | None = None


class WebSocketNotification(TwitchBaseModel):
    """WebSocket notification message."""

    subscription: EventSubSubscription
    event: dict


class WebSocketReconnect(TwitchBaseModel):
    """WebSocket reconnect message."""

    session_id: str
    status: str
    reconnect_url: str


class WebSocketRevocation(TwitchBaseModel):
    """WebSocket subscription revocation message."""

    subscription: EventSubSubscription


# Conduit schemas
class Conduit(TwitchBaseModel):
    """Conduit data."""

    id: str
    shard_count: int


class GetConduitsRequest(TwitchBaseModel):
    """Request params for Get Conduits (no params needed)."""

    pass


class CreateConduitRequest(TwitchBaseModel):
    """Request to create a conduit."""

    shard_count: int = Field(ge=1)


class UpdateConduitRequest(TwitchBaseModel):
    """Request to update a conduit."""

    id: str
    shard_count: int = Field(ge=1)


class DeleteConduitRequest(TwitchBaseModel):
    """Request to delete a conduit."""

    id: str


class ConduitShardTransport(TwitchBaseModel):
    """Conduit shard transport config."""

    method: str
    callback: str | None = None
    session_id: str | None = None


class ConduitShard(TwitchBaseModel):
    """Conduit shard data."""

    id: str
    status: str
    transport: ConduitShardTransport


class GetConduitShardsRequest(TwitchBaseModel):
    """Request params for Get Conduit Shards."""

    conduit_id: str
    status: str | None = None
    after: str | None = None


class UpdateConduitShardsRequest(TwitchBaseModel):
    """Request to update conduit shards."""

    conduit_id: str
    shards: list[dict]
