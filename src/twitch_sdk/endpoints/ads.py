"""Ads endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.ads import (
    AdSchedule,
    GetAdScheduleRequest,
    SnoozeNextAdRequest,
    SnoozeNextAdResponse,
    StartCommercialRequest,
    StartCommercialResponse,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def start_commercial(
    client: "TwitchHTTPClient",
    params: StartCommercialRequest,
) -> TwitchResponse[StartCommercialResponse]:
    """Start a commercial on a channel.

    Requires channel:edit:commercial scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post("/channels/commercial", data=data)
    return TwitchResponse[StartCommercialResponse].model_validate(response)


async def get_ad_schedule(
    client: "TwitchHTTPClient",
    params: GetAdScheduleRequest,
) -> TwitchResponse[AdSchedule]:
    """Get ad schedule for a channel.

    Requires channel:read:ads scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels/ads", params=query)
    return TwitchResponse[AdSchedule].model_validate(response)


async def snooze_next_ad(
    client: "TwitchHTTPClient",
    params: SnoozeNextAdRequest,
) -> TwitchResponse[SnoozeNextAdResponse]:
    """Snooze the next ad break.

    Requires channel:manage:ads scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.post("/channels/ads/schedule/snooze", params=query)
    return TwitchResponse[SnoozeNextAdResponse].model_validate(response)
