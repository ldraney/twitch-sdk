"""Moderation endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.moderation import (
    AddBlockedTermRequest,
    AddModeratorRequest,
    AutoModSettings,
    BannedUser,
    BanUserRequest,
    BanUserResponse,
    BlockedTerm,
    DeleteChatMessagesRequest,
    GetAutoModSettingsRequest,
    GetBannedUsersRequest,
    GetBlockedTermsRequest,
    GetModeratorsRequest,
    GetShieldModeStatusRequest,
    GetUnbanRequestsRequest,
    ManageHeldAutoModMessageRequest,
    Moderator,
    RemoveBlockedTermRequest,
    RemoveModeratorRequest,
    ResolveUnbanRequestRequest,
    ShieldModeStatus,
    UnbanRequest,
    UnbanUserRequest,
    UpdateAutoModSettingsRequest,
    UpdateShieldModeStatusRequest,
    WarnUserRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_banned_users(
    client: "TwitchHTTPClient",
    params: GetBannedUsersRequest,
) -> TwitchResponse[BannedUser]:
    """Get list of banned users for a channel.

    Requires moderation:read scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/banned", params=query)
    return TwitchResponse[BannedUser].model_validate(response)


async def ban_user(
    client: "TwitchHTTPClient",
    params: BanUserRequest,
) -> TwitchResponse[BanUserResponse]:
    """Ban a user from a channel.

    Requires moderator:manage:banned_users scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = {"data": params.data.model_dump(exclude_none=True)}
    response = await client.post("/moderation/bans", params=query, data=data)
    return TwitchResponse[BanUserResponse].model_validate(response)


async def unban_user(
    client: "TwitchHTTPClient",
    params: UnbanUserRequest,
) -> None:
    """Unban a user from a channel.

    Requires moderator:manage:banned_users scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/moderation/bans", params=query)


async def get_unban_requests(
    client: "TwitchHTTPClient",
    params: GetUnbanRequestsRequest,
) -> TwitchResponse[UnbanRequest]:
    """Get unban requests for a channel.

    Requires moderator:read:unban_requests scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/unban_requests", params=query)
    return TwitchResponse[UnbanRequest].model_validate(response)


async def resolve_unban_request(
    client: "TwitchHTTPClient",
    params: ResolveUnbanRequestRequest,
) -> TwitchResponse[UnbanRequest]:
    """Resolve an unban request.

    Requires moderator:manage:unban_requests scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.patch("/moderation/unban_requests", params=query)
    return TwitchResponse[UnbanRequest].model_validate(response)


async def get_blocked_terms(
    client: "TwitchHTTPClient",
    params: GetBlockedTermsRequest,
) -> TwitchResponse[BlockedTerm]:
    """Get blocked terms for a channel.

    Requires moderator:read:blocked_terms scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/blocked_terms", params=query)
    return TwitchResponse[BlockedTerm].model_validate(response)


async def add_blocked_term(
    client: "TwitchHTTPClient",
    params: AddBlockedTermRequest,
) -> TwitchResponse[BlockedTerm]:
    """Add a blocked term to a channel.

    Requires moderator:manage:blocked_terms scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = {"text": params.text}
    response = await client.post("/moderation/blocked_terms", params=query, data=data)
    return TwitchResponse[BlockedTerm].model_validate(response)


async def remove_blocked_term(
    client: "TwitchHTTPClient",
    params: RemoveBlockedTermRequest,
) -> None:
    """Remove a blocked term from a channel.

    Requires moderator:manage:blocked_terms scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/moderation/blocked_terms", params=query)


async def get_automod_settings(
    client: "TwitchHTTPClient",
    params: GetAutoModSettingsRequest,
) -> TwitchResponse[AutoModSettings]:
    """Get AutoMod settings for a channel.

    Requires moderator:read:automod_settings scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/automod/settings", params=query)
    return TwitchResponse[AutoModSettings].model_validate(response)


async def update_automod_settings(
    client: "TwitchHTTPClient",
    params: UpdateAutoModSettingsRequest,
) -> TwitchResponse[AutoModSettings]:
    """Update AutoMod settings for a channel.

    Requires moderator:manage:automod_settings scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = params.model_dump(exclude={"broadcaster_id", "moderator_id"}, exclude_none=True)
    response = await client.put("/moderation/automod/settings", params=query, data=data)
    return TwitchResponse[AutoModSettings].model_validate(response)


async def manage_held_automod_message(
    client: "TwitchHTTPClient",
    params: ManageHeldAutoModMessageRequest,
) -> None:
    """Allow or deny a message held by AutoMod.

    Requires moderator:manage:automod scope.
    """
    data = params.model_dump(exclude_none=True)
    await client.post("/moderation/automod/message", data=data)


async def get_moderators(
    client: "TwitchHTTPClient",
    params: GetModeratorsRequest,
) -> TwitchResponse[Moderator]:
    """Get list of moderators for a channel.

    Requires moderation:read scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/moderators", params=query)
    return TwitchResponse[Moderator].model_validate(response)


async def add_moderator(
    client: "TwitchHTTPClient",
    params: AddModeratorRequest,
) -> None:
    """Add a moderator to a channel.

    Requires channel:manage:moderators scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.post("/moderation/moderators", params=query)


async def remove_moderator(
    client: "TwitchHTTPClient",
    params: RemoveModeratorRequest,
) -> None:
    """Remove a moderator from a channel.

    Requires channel:manage:moderators scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/moderation/moderators", params=query)


async def get_shield_mode_status(
    client: "TwitchHTTPClient",
    params: GetShieldModeStatusRequest,
) -> TwitchResponse[ShieldModeStatus]:
    """Get shield mode status for a channel.

    Requires moderator:read:shield_mode scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/moderation/shield_mode", params=query)
    return TwitchResponse[ShieldModeStatus].model_validate(response)


async def update_shield_mode_status(
    client: "TwitchHTTPClient",
    params: UpdateShieldModeStatusRequest,
) -> TwitchResponse[ShieldModeStatus]:
    """Update shield mode status for a channel.

    Requires moderator:manage:shield_mode scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = {"is_active": params.is_active}
    response = await client.put("/moderation/shield_mode", params=query, data=data)
    return TwitchResponse[ShieldModeStatus].model_validate(response)


async def warn_chat_user(
    client: "TwitchHTTPClient",
    params: WarnUserRequest,
) -> None:
    """Warn a user in chat.

    Requires moderator:manage:warnings scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "moderator_id": params.moderator_id}
    data = {"user_id": params.user_id, "reason": params.reason}
    await client.post("/moderation/warnings", params=query, data=data)


async def delete_chat_messages(
    client: "TwitchHTTPClient",
    params: DeleteChatMessagesRequest,
) -> None:
    """Delete chat messages.

    Requires moderator:manage:chat_messages scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/moderation/chat", params=query)
