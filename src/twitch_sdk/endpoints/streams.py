"""Streams endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.streams import (
    CreateStreamMarkerRequest,
    CreateStreamMarkerResponse,
    GetFollowedStreamsRequest,
    GetStreamKeyRequest,
    GetStreamMarkersRequest,
    GetStreamsRequest,
    Stream,
    StreamKey,
    UserMarkers,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_streams(
    client: "TwitchHTTPClient",
    params: GetStreamsRequest | None = None,
) -> TwitchResponse[Stream]:
    """Get active streams.

    Returns list of streams matching the query parameters.
    """
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/streams", params=query)
    return TwitchResponse[Stream].model_validate(response)


async def get_followed_streams(
    client: "TwitchHTTPClient",
    params: GetFollowedStreamsRequest,
) -> TwitchResponse[Stream]:
    """Get streams from channels that the user follows."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/streams/followed", params=query)
    return TwitchResponse[Stream].model_validate(response)


async def create_stream_marker(
    client: "TwitchHTTPClient",
    params: CreateStreamMarkerRequest,
) -> TwitchResponse[CreateStreamMarkerResponse]:
    """Create a marker in a live stream.

    Requires user:edit:broadcast scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post("/streams/markers", data=data)
    return TwitchResponse[CreateStreamMarkerResponse].model_validate(response)


async def get_stream_markers(
    client: "TwitchHTTPClient",
    params: GetStreamMarkersRequest,
) -> TwitchResponse[UserMarkers]:
    """Get stream markers for a VOD or live stream."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/streams/markers", params=query)
    return TwitchResponse[UserMarkers].model_validate(response)


async def get_stream_key(
    client: "TwitchHTTPClient",
    params: GetStreamKeyRequest,
) -> TwitchResponse[StreamKey]:
    """Get the channel's stream key.

    Requires channel:read:stream_key scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/streams/key", params=query)
    return TwitchResponse[StreamKey].model_validate(response)
