"""EventSub endpoints and WebSocket handler."""

import asyncio
import json
from typing import TYPE_CHECKING, AsyncGenerator

import websockets

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.eventsub import (
    Conduit,
    ConduitShard,
    CreateConduitRequest,
    CreateEventSubSubscriptionRequest,
    DeleteConduitRequest,
    DeleteEventSubSubscriptionRequest,
    EventSubSubscription,
    GetConduitShardsRequest,
    GetEventSubSubscriptionsRequest,
    GetEventSubSubscriptionsResponse,
    UpdateConduitRequest,
    UpdateConduitShardsRequest,
    WebSocketNotification,
    WebSocketWelcome,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


# HTTP API Endpoints

async def create_eventsub_subscription(
    client: "TwitchHTTPClient",
    params: CreateEventSubSubscriptionRequest,
) -> TwitchResponse[EventSubSubscription]:
    """Create an EventSub subscription."""
    data = params.model_dump(exclude_none=True)
    response = await client.post("/eventsub/subscriptions", data=data)
    return TwitchResponse[EventSubSubscription].model_validate(response)


async def delete_eventsub_subscription(
    client: "TwitchHTTPClient",
    params: DeleteEventSubSubscriptionRequest,
) -> None:
    """Delete an EventSub subscription."""
    query = params.model_dump(exclude_none=True)
    await client.delete("/eventsub/subscriptions", params=query)


async def get_eventsub_subscriptions(
    client: "TwitchHTTPClient",
    params: GetEventSubSubscriptionsRequest | None = None,
) -> GetEventSubSubscriptionsResponse:
    """Get list of EventSub subscriptions."""
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/eventsub/subscriptions", params=query)
    return GetEventSubSubscriptionsResponse.model_validate(response)


# Conduit endpoints

async def get_conduits(
    client: "TwitchHTTPClient",
) -> TwitchResponse[Conduit]:
    """Get list of conduits.

    Note: Requires app access token (not user token).
    """
    response = await client.get_app("/eventsub/conduits")
    return TwitchResponse[Conduit].model_validate(response)


async def create_conduit(
    client: "TwitchHTTPClient",
    params: CreateConduitRequest,
) -> TwitchResponse[Conduit]:
    """Create a conduit.

    Note: Requires app access token (not user token).
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post_app("/eventsub/conduits", data=data)
    return TwitchResponse[Conduit].model_validate(response)


async def update_conduit(
    client: "TwitchHTTPClient",
    params: UpdateConduitRequest,
) -> TwitchResponse[Conduit]:
    """Update a conduit's shard count.

    Note: Requires app access token (not user token).
    """
    data = params.model_dump(exclude_none=True)
    response = await client.patch_app("/eventsub/conduits", data=data)
    return TwitchResponse[Conduit].model_validate(response)


async def delete_conduit(
    client: "TwitchHTTPClient",
    params: DeleteConduitRequest,
) -> None:
    """Delete a conduit.

    Note: Requires app access token (not user token).
    """
    query = params.model_dump(exclude_none=True)
    await client.delete_app("/eventsub/conduits", params=query)


async def get_conduit_shards(
    client: "TwitchHTTPClient",
    params: GetConduitShardsRequest,
) -> TwitchResponse[ConduitShard]:
    """Get shards for a conduit.

    Note: Requires app access token (not user token).
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get_app("/eventsub/conduits/shards", params=query)
    return TwitchResponse[ConduitShard].model_validate(response)


async def update_conduit_shards(
    client: "TwitchHTTPClient",
    params: UpdateConduitShardsRequest,
) -> TwitchResponse[ConduitShard]:
    """Update conduit shards.

    Note: Requires app access token (not user token).
    """
    data = params.model_dump(exclude_none=True)
    response = await client.patch_app("/eventsub/conduits/shards", data=data)
    return TwitchResponse[ConduitShard].model_validate(response)


# WebSocket client for EventSub

class EventSubWebSocket:
    """WebSocket client for Twitch EventSub.

    Connects to Twitch EventSub WebSocket, handles session management,
    and yields incoming events.
    """

    EVENTSUB_WSS_URL = "wss://eventsub.wss.twitch.tv/ws"

    def __init__(self, client: "TwitchHTTPClient"):
        """Initialize EventSub WebSocket.

        Args:
            client: TwitchHTTPClient for making API calls.
        """
        self.client = client
        self._ws = None
        self._session_id: str | None = None
        self._keepalive_timeout: int = 10
        self._reconnect_url: str | None = None
        self._subscriptions: list[str] = []

    @property
    def session_id(self) -> str | None:
        """Get the current session ID."""
        return self._session_id

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._ws is not None and self._ws.open

    async def connect(self) -> str:
        """Connect to EventSub WebSocket.

        Returns:
            Session ID for creating subscriptions.
        """
        url = self._reconnect_url or self.EVENTSUB_WSS_URL
        self._ws = await websockets.connect(url)

        # Wait for welcome message
        raw_message = await self._ws.recv()
        message = json.loads(raw_message)

        if message.get("metadata", {}).get("message_type") != "session_welcome":
            raise RuntimeError(f"Expected session_welcome, got: {message}")

        payload = message.get("payload", {}).get("session", {})
        welcome = WebSocketWelcome.model_validate(payload)

        self._session_id = welcome.session_id
        self._keepalive_timeout = welcome.keepalive_timeout_seconds
        self._reconnect_url = welcome.reconnect_url

        return self._session_id

    async def subscribe(
        self,
        event_type: str,
        version: str,
        condition: dict,
    ) -> EventSubSubscription:
        """Subscribe to an EventSub event type.

        Args:
            event_type: The event type (e.g., "channel.chat.message").
            version: The subscription version.
            condition: The condition for the subscription.

        Returns:
            The created subscription.
        """
        if not self._session_id:
            raise RuntimeError("Not connected. Call connect() first.")

        params = CreateEventSubSubscriptionRequest(
            type=event_type,
            version=version,
            condition=condition,
            transport={
                "method": "websocket",
                "session_id": self._session_id,
            },
        )

        result = await create_eventsub_subscription(self.client, params)
        subscription = result.data[0]
        self._subscriptions.append(subscription.id)
        return subscription

    async def events(self) -> AsyncGenerator[dict, None]:
        """Async generator that yields EventSub events.

        Handles keepalive messages internally.
        Yields event payloads for notification messages.
        """
        if not self._ws:
            raise RuntimeError("Not connected. Call connect() first.")

        while True:
            try:
                raw_message = await asyncio.wait_for(
                    self._ws.recv(),
                    timeout=self._keepalive_timeout + 10,
                )
            except asyncio.TimeoutError:
                # No message received, connection may be dead
                break

            message = json.loads(raw_message)
            message_type = message.get("metadata", {}).get("message_type")

            if message_type == "session_keepalive":
                # Keepalive, continue
                continue

            elif message_type == "notification":
                # Yield the event
                payload = message.get("payload", {})
                yield payload

            elif message_type == "session_reconnect":
                # Handle reconnection
                payload = message.get("payload", {}).get("session", {})
                self._reconnect_url = payload.get("reconnect_url")
                await self._ws.close()
                await self.connect()

            elif message_type == "revocation":
                # Subscription was revoked
                payload = message.get("payload", {})
                yield {"revocation": payload}

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._ws:
            await self._ws.close()
            self._ws = None
            self._session_id = None

    async def __aenter__(self) -> "EventSubWebSocket":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
