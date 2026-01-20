"""Clips endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.clips import (
    Clip,
    CreateClipRequest,
    CreateClipResponse,
    GetClipsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def create_clip(
    client: "TwitchHTTPClient",
    params: CreateClipRequest,
) -> TwitchResponse[CreateClipResponse]:
    """Create a clip from the broadcaster's stream.

    Requires clips:edit scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.post("/clips", params=query)
    return TwitchResponse[CreateClipResponse].model_validate(response)


async def get_clips(
    client: "TwitchHTTPClient",
    params: GetClipsRequest,
) -> TwitchResponse[Clip]:
    """Get clips for a broadcaster, game, or specific clip IDs."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/clips", params=query)
    return TwitchResponse[Clip].model_validate(response)
