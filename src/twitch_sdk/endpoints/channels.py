"""Channels endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.channels import (
    AddVIPRequest,
    Channel,
    ChannelEditor,
    FollowedChannel,
    Follower,
    GetChannelEditorsRequest,
    GetChannelFollowersRequest,
    GetChannelFollowersResponse,
    GetChannelInfoRequest,
    GetFollowedChannelsRequest,
    GetVIPsRequest,
    ModifyChannelInfoRequest,
    RemoveVIPRequest,
    VIP,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_channel_information(
    client: "TwitchHTTPClient",
    params: GetChannelInfoRequest,
) -> TwitchResponse[Channel]:
    """Get channel information for one or more broadcasters."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels", params=query)
    return TwitchResponse[Channel].model_validate(response)


async def modify_channel_information(
    client: "TwitchHTTPClient",
    params: ModifyChannelInfoRequest,
) -> None:
    """Modify channel information.

    Requires channel:manage:broadcast scope.
    """
    query = {"broadcaster_id": params.broadcaster_id}
    data = params.model_dump(exclude={"broadcaster_id"}, exclude_none=True)
    await client.patch("/channels", params=query, data=data)


async def get_channel_editors(
    client: "TwitchHTTPClient",
    params: GetChannelEditorsRequest,
) -> TwitchResponse[ChannelEditor]:
    """Get list of channel editors.

    Requires channel:read:editors scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels/editors", params=query)
    return TwitchResponse[ChannelEditor].model_validate(response)


async def get_followed_channels(
    client: "TwitchHTTPClient",
    params: GetFollowedChannelsRequest,
) -> TwitchResponse[FollowedChannel]:
    """Get channels that a user follows.

    Requires user:read:follows scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels/followed", params=query)
    return TwitchResponse[FollowedChannel].model_validate(response)


async def get_channel_followers(
    client: "TwitchHTTPClient",
    params: GetChannelFollowersRequest,
) -> GetChannelFollowersResponse:
    """Get list of users that follow a channel.

    Requires moderator:read:followers scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels/followers", params=query)
    return GetChannelFollowersResponse.model_validate(response)


async def get_vips(
    client: "TwitchHTTPClient",
    params: GetVIPsRequest,
) -> TwitchResponse[VIP]:
    """Get list of VIPs for a channel.

    Requires channel:read:vips or channel:manage:vips scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channels/vips", params=query)
    return TwitchResponse[VIP].model_validate(response)


async def add_channel_vip(
    client: "TwitchHTTPClient",
    params: AddVIPRequest,
) -> None:
    """Add a VIP to the channel.

    Requires channel:manage:vips scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.post("/channels/vips", params=query)


async def remove_channel_vip(
    client: "TwitchHTTPClient",
    params: RemoveVIPRequest,
) -> None:
    """Remove a VIP from the channel.

    Requires channel:manage:vips scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/channels/vips", params=query)
