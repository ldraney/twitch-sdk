"""Analytics endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.analytics import (
    ExtensionAnalytics,
    GameAnalytics,
    GetExtensionAnalyticsRequest,
    GetGameAnalyticsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_extension_analytics(
    client: "TwitchHTTPClient",
    params: GetExtensionAnalyticsRequest | None = None,
) -> TwitchResponse[ExtensionAnalytics]:
    """Get analytics for extensions.

    Requires analytics:read:extensions scope.
    """
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/analytics/extensions", params=query)
    return TwitchResponse[ExtensionAnalytics].model_validate(response)


async def get_game_analytics(
    client: "TwitchHTTPClient",
    params: GetGameAnalyticsRequest | None = None,
) -> TwitchResponse[GameAnalytics]:
    """Get analytics for games.

    Requires analytics:read:games scope.
    """
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/analytics/games", params=query)
    return TwitchResponse[GameAnalytics].model_validate(response)
