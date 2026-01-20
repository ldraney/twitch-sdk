"""Polls endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.polls import (
    CreatePollRequest,
    EndPollRequest,
    GetPollsRequest,
    Poll,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_polls(
    client: "TwitchHTTPClient",
    params: GetPollsRequest,
) -> TwitchResponse[Poll]:
    """Get polls for a channel.

    Requires channel:read:polls scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/polls", params=query)
    return TwitchResponse[Poll].model_validate(response)


async def create_poll(
    client: "TwitchHTTPClient",
    params: CreatePollRequest,
) -> TwitchResponse[Poll]:
    """Create a poll on a channel.

    Requires channel:manage:polls scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post("/polls", data=data)
    return TwitchResponse[Poll].model_validate(response)


async def end_poll(
    client: "TwitchHTTPClient",
    params: EndPollRequest,
) -> TwitchResponse[Poll]:
    """End an active poll.

    Requires channel:manage:polls scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.patch("/polls", data=data)
    return TwitchResponse[Poll].model_validate(response)
