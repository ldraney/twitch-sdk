"""Guest Star endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.guest_star import (
    AssignGuestStarSlotRequest,
    CreateGuestStarSessionRequest,
    DeleteGuestStarInviteRequest,
    DeleteGuestStarSlotRequest,
    EndGuestStarSessionRequest,
    GetGuestStarInvitesRequest,
    GetGuestStarSessionRequest,
    GetGuestStarSettingsRequest,
    GuestStarInvite,
    GuestStarSession,
    GuestStarSettings,
    SendGuestStarInviteRequest,
    UpdateGuestStarSettingsRequest,
    UpdateGuestStarSlotRequest,
    UpdateGuestStarSlotSettingsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_channel_guest_star_settings(
    client: "TwitchHTTPClient",
    params: GetGuestStarSettingsRequest,
) -> TwitchResponse[GuestStarSettings]:
    """Get guest star settings for a channel.

    Requires channel:read:guest_star or channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/guest_star/channel_settings", params=query)
    return TwitchResponse[GuestStarSettings].model_validate(response)


async def update_channel_guest_star_settings(
    client: "TwitchHTTPClient",
    params: UpdateGuestStarSettingsRequest,
) -> None:
    """Update guest star settings for a channel.

    Requires channel:manage:guest_star scope.
    """
    query = {"broadcaster_id": params.broadcaster_id}
    data = params.model_dump(exclude={"broadcaster_id"}, exclude_none=True)
    await client.put("/guest_star/channel_settings", params=query, data=data)


async def get_guest_star_session(
    client: "TwitchHTTPClient",
    params: GetGuestStarSessionRequest,
) -> TwitchResponse[GuestStarSession]:
    """Get active guest star session for a channel.

    Requires channel:read:guest_star or channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/guest_star/session", params=query)
    return TwitchResponse[GuestStarSession].model_validate(response)


async def create_guest_star_session(
    client: "TwitchHTTPClient",
    params: CreateGuestStarSessionRequest,
) -> TwitchResponse[GuestStarSession]:
    """Create a guest star session.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.post("/guest_star/session", params=query)
    return TwitchResponse[GuestStarSession].model_validate(response)


async def end_guest_star_session(
    client: "TwitchHTTPClient",
    params: EndGuestStarSessionRequest,
) -> TwitchResponse[GuestStarSession]:
    """End a guest star session.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.delete("/guest_star/session", params=query)
    return TwitchResponse[GuestStarSession].model_validate(response)


async def get_guest_star_invites(
    client: "TwitchHTTPClient",
    params: GetGuestStarInvitesRequest,
) -> TwitchResponse[GuestStarInvite]:
    """Get guest star invites for a session.

    Requires channel:read:guest_star or channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/guest_star/invites", params=query)
    return TwitchResponse[GuestStarInvite].model_validate(response)


async def send_guest_star_invite(
    client: "TwitchHTTPClient",
    params: SendGuestStarInviteRequest,
) -> None:
    """Send a guest star invite.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.post("/guest_star/invites", params=query)


async def delete_guest_star_invite(
    client: "TwitchHTTPClient",
    params: DeleteGuestStarInviteRequest,
) -> None:
    """Delete a guest star invite.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/guest_star/invites", params=query)


async def assign_guest_star_slot(
    client: "TwitchHTTPClient",
    params: AssignGuestStarSlotRequest,
) -> None:
    """Assign a guest to a slot.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.post("/guest_star/slot", params=query)


async def update_guest_star_slot(
    client: "TwitchHTTPClient",
    params: UpdateGuestStarSlotRequest,
) -> None:
    """Move a guest between slots.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.patch("/guest_star/slot", params=query)


async def delete_guest_star_slot(
    client: "TwitchHTTPClient",
    params: DeleteGuestStarSlotRequest,
) -> None:
    """Remove a guest from a slot.

    Requires channel:manage:guest_star scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/guest_star/slot", params=query)


async def update_guest_star_slot_settings(
    client: "TwitchHTTPClient",
    params: UpdateGuestStarSlotSettingsRequest,
) -> None:
    """Update slot settings (audio/video/volume).

    Requires channel:manage:guest_star scope.
    """
    query = {
        "broadcaster_id": params.broadcaster_id,
        "moderator_id": params.moderator_id,
        "session_id": params.session_id,
        "slot_id": params.slot_id,
    }
    data = params.model_dump(
        exclude={"broadcaster_id", "moderator_id", "session_id", "slot_id"},
        exclude_none=True,
    )
    await client.patch("/guest_star/slot_settings", params=query, data=data)
