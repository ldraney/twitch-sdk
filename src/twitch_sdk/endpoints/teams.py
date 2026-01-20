"""Teams endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.teams import (
    GetChannelTeamsRequest,
    GetTeamsRequest,
    Team,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_teams(
    client: "TwitchHTTPClient",
    params: GetTeamsRequest,
) -> TwitchResponse[Team]:
    """Get information about a team."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/teams", params=query)
    return TwitchResponse[Team].model_validate(response)


async def get_channel_teams(
    client: "TwitchHTTPClient",
    params: GetChannelTeamsRequest,
) -> TwitchResponse[Team]:
    """Get teams that a broadcaster is a member of."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/teams/channel", params=query)
    return TwitchResponse[Team].model_validate(response)
