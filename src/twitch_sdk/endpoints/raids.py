"""Raids endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.raids import (
    CancelRaidRequest,
    StartRaidRequest,
    StartRaidResponse,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def start_raid(
    client: "TwitchHTTPClient",
    params: StartRaidRequest,
) -> TwitchResponse[StartRaidResponse]:
    """Start a raid to another channel.

    Requires channel:manage:raids scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.post("/raids", params=query)
    return TwitchResponse[StartRaidResponse].model_validate(response)


async def cancel_raid(
    client: "TwitchHTTPClient",
    params: CancelRaidRequest,
) -> None:
    """Cancel a pending raid.

    Requires channel:manage:raids scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/raids", params=query)
