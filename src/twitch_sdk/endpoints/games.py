"""Games endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.games import (
    Game,
    GetGamesRequest,
    GetTopGamesRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_games(
    client: "TwitchHTTPClient",
    params: GetGamesRequest,
) -> TwitchResponse[Game]:
    """Get games by ID, name, or IGDB ID."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/games", params=query)
    return TwitchResponse[Game].model_validate(response)


async def get_top_games(
    client: "TwitchHTTPClient",
    params: GetTopGamesRequest | None = None,
) -> TwitchResponse[Game]:
    """Get top games by viewer count."""
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/games/top", params=query)
    return TwitchResponse[Game].model_validate(response)
