"""Goals endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.goals import GetGoalsRequest, Goal

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_creator_goals(
    client: "TwitchHTTPClient",
    params: GetGoalsRequest,
) -> TwitchResponse[Goal]:
    """Get the broadcaster's active creator goals.

    Requires channel:read:goals scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/goals", params=query)
    return TwitchResponse[Goal].model_validate(response)
