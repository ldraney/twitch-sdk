"""Chat endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.chat import (
    Badge,
    ChatSettings,
    Chatter,
    Emote,
    GetBadgesRequest,
    GetChatSettingsRequest,
    GetChattersRequest,
    GetChattersResponse,
    GetEmoteSetsRequest,
    GetEmotesRequest,
    GetShoutoutsRequest,
    GetUserChatColorRequest,
    SendAnnouncementRequest,
    SendMessageRequest,
    SendMessageResponse,
    ShoutoutRequest,
    UpdateChatSettingsRequest,
    UpdateUserChatColorRequest,
    UserChatColor,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_chatters(
    client: "TwitchHTTPClient",
    params: GetChattersRequest,
) -> GetChattersResponse:
    """Get list of users in the broadcaster's chat.

    Requires moderator:read:chatters scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/chatters", params=query)
    return GetChattersResponse.model_validate(response)


async def get_channel_emotes(
    client: "TwitchHTTPClient",
    params: GetEmotesRequest,
) -> TwitchResponse[Emote]:
    """Get channel's custom emotes."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/emotes", params=query)
    return TwitchResponse[Emote].model_validate(response)


async def get_global_emotes(
    client: "TwitchHTTPClient",
) -> TwitchResponse[Emote]:
    """Get global emotes."""
    response = await client.get("/chat/emotes/global")
    return TwitchResponse[Emote].model_validate(response)


async def get_emote_sets(
    client: "TwitchHTTPClient",
    params: GetEmoteSetsRequest,
) -> TwitchResponse[Emote]:
    """Get emotes from specific emote sets."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/emotes/set", params=query)
    return TwitchResponse[Emote].model_validate(response)


async def get_channel_chat_badges(
    client: "TwitchHTTPClient",
    params: GetBadgesRequest,
) -> TwitchResponse[Badge]:
    """Get channel's chat badges."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/badges", params=query)
    return TwitchResponse[Badge].model_validate(response)


async def get_global_chat_badges(
    client: "TwitchHTTPClient",
) -> TwitchResponse[Badge]:
    """Get global chat badges."""
    response = await client.get("/chat/badges/global")
    return TwitchResponse[Badge].model_validate(response)


async def get_chat_settings(
    client: "TwitchHTTPClient",
    params: GetChatSettingsRequest,
) -> TwitchResponse[ChatSettings]:
    """Get chat settings for a channel."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/settings", params=query)
    return TwitchResponse[ChatSettings].model_validate(response)


async def update_chat_settings(
    client: "TwitchHTTPClient",
    params: UpdateChatSettingsRequest,
) -> TwitchResponse[ChatSettings]:
    """Update chat settings for a channel.

    Requires moderator:manage:chat_settings scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = params.model_dump(exclude={"broadcaster_id", "moderator_id"}, exclude_none=True)
    response = await client.patch("/chat/settings", params=query, data=data)
    return TwitchResponse[ChatSettings].model_validate(response)


async def send_chat_announcement(
    client: "TwitchHTTPClient",
    params: SendAnnouncementRequest,
) -> None:
    """Send an announcement to the chat.

    Requires moderator:manage:announcements scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = {"message": params.message}
    if params.color:
        data["color"] = params.color
    await client.post("/chat/announcements", params=query, data=data)


async def send_shoutout(
    client: "TwitchHTTPClient",
    params: ShoutoutRequest,
) -> None:
    """Send a shoutout to another broadcaster.

    Requires moderator:manage:shoutouts scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.post("/chat/shoutouts", params=query)


async def get_user_chat_color(
    client: "TwitchHTTPClient",
    params: GetUserChatColorRequest,
) -> TwitchResponse[UserChatColor]:
    """Get the color used for users' names in chat."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/chat/color", params=query)
    return TwitchResponse[UserChatColor].model_validate(response)


async def update_user_chat_color(
    client: "TwitchHTTPClient",
    params: UpdateUserChatColorRequest,
) -> None:
    """Update the user's chat color.

    Requires user:manage:chat_color scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.put("/chat/color", params=query)


async def send_chat_message(
    client: "TwitchHTTPClient",
    params: SendMessageRequest,
) -> TwitchResponse[SendMessageResponse]:
    """Send a chat message to a broadcaster's chat.

    Requires user:write:chat scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post("/chat/messages", data=data)
    return TwitchResponse[SendMessageResponse].model_validate(response)


# Alias for common naming convention
send_announcement = send_chat_announcement
