"""Hype Train endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.hype_train import GetHypeTrainEventsRequest, HypeTrainEvent

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_hype_train_events(
    client: "TwitchHTTPClient",
    params: GetHypeTrainEventsRequest,
) -> TwitchResponse[HypeTrainEvent]:
    """Get hype train events for a broadcaster.

    Requires channel:read:hype_train scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/hypetrain/events", params=query)
    return TwitchResponse[HypeTrainEvent].model_validate(response)
