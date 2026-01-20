"""Main Twitch SDK client."""

from twitch_client import TwitchAuth, TwitchCredentials, TwitchHTTPClient

from . import endpoints
from .endpoints.eventsub import EventSubWebSocket


class TwitchSDK:
    """Main Twitch SDK client.

    Provides access to all Twitch Helix API endpoints through
    a unified interface with Pydantic validation.
    """

    def __init__(
        self,
        credentials: TwitchCredentials | None = None,
        http_client: TwitchHTTPClient | None = None,
    ):
        """Initialize the SDK.

        Args:
            credentials: Twitch credentials. If None, loads from environment.
            http_client: Pre-configured HTTP client. If None, creates one.
        """
        if http_client:
            self._client = http_client
            self._owns_client = False
        else:
            self._client = TwitchHTTPClient(credentials=credentials)
            self._owns_client = True

    @property
    def http(self) -> TwitchHTTPClient:
        """Get the underlying HTTP client."""
        return self._client

    # Endpoint access
    @property
    def ads(self):
        """Access Ads endpoints."""
        return endpoints.ads

    @property
    def analytics(self):
        """Access Analytics endpoints."""
        return endpoints.analytics

    @property
    def bits(self):
        """Access Bits endpoints."""
        return endpoints.bits

    @property
    def channel_points(self):
        """Access Channel Points endpoints."""
        return endpoints.channel_points

    @property
    def channels(self):
        """Access Channels endpoints."""
        return endpoints.channels

    @property
    def charity(self):
        """Access Charity endpoints."""
        return endpoints.charity

    @property
    def chat(self):
        """Access Chat endpoints."""
        return endpoints.chat

    @property
    def clips(self):
        """Access Clips endpoints."""
        return endpoints.clips

    @property
    def eventsub(self):
        """Access EventSub endpoints."""
        return endpoints.eventsub

    @property
    def games(self):
        """Access Games endpoints."""
        return endpoints.games

    @property
    def goals(self):
        """Access Goals endpoints."""
        return endpoints.goals

    @property
    def guest_star(self):
        """Access Guest Star endpoints."""
        return endpoints.guest_star

    @property
    def hype_train(self):
        """Access Hype Train endpoints."""
        return endpoints.hype_train

    @property
    def moderation(self):
        """Access Moderation endpoints."""
        return endpoints.moderation

    @property
    def polls(self):
        """Access Polls endpoints."""
        return endpoints.polls

    @property
    def predictions(self):
        """Access Predictions endpoints."""
        return endpoints.predictions

    @property
    def raids(self):
        """Access Raids endpoints."""
        return endpoints.raids

    @property
    def schedule(self):
        """Access Schedule endpoints."""
        return endpoints.schedule

    @property
    def search(self):
        """Access Search endpoints."""
        return endpoints.search

    @property
    def streams(self):
        """Access Streams endpoints."""
        return endpoints.streams

    @property
    def subscriptions(self):
        """Access Subscriptions endpoints."""
        return endpoints.subscriptions

    @property
    def teams(self):
        """Access Teams endpoints."""
        return endpoints.teams

    @property
    def users(self):
        """Access Users endpoints."""
        return endpoints.users

    @property
    def videos(self):
        """Access Videos endpoints."""
        return endpoints.videos

    @property
    def whispers(self):
        """Access Whispers endpoints."""
        return endpoints.whispers

    def create_eventsub_websocket(self) -> EventSubWebSocket:
        """Create an EventSub WebSocket client.

        Returns:
            EventSubWebSocket instance for subscribing to real-time events.
        """
        return EventSubWebSocket(self._client)

    async def close(self) -> None:
        """Close the SDK and release resources."""
        if self._owns_client:
            await self._client.close()

    async def __aenter__(self) -> "TwitchSDK":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
