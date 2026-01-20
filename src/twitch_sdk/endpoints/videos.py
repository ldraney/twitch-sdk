"""Videos endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.videos import (
    DeleteVideosRequest,
    GetVideosRequest,
    Video,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_videos(
    client: "TwitchHTTPClient",
    params: GetVideosRequest,
) -> TwitchResponse[Video]:
    """Get videos by ID, user, or game."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/videos", params=query)
    return TwitchResponse[Video].model_validate(response)


async def delete_videos(
    client: "TwitchHTTPClient",
    params: DeleteVideosRequest,
) -> list[str]:
    """Delete videos.

    Requires channel:manage:videos scope.
    Returns list of deleted video IDs.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.delete("/videos", params=query)
    return response.get("data", [])
