"""Users endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.users import (
    BlockUserRequest,
    GetUserBlockListRequest,
    GetUsersRequest,
    UnblockUserRequest,
    UpdateUserExtensionsRequest,
    UpdateUserRequest,
    User,
    UserActiveExtensions,
    UserBlockTarget,
    UserExtension,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_users(
    client: "TwitchHTTPClient",
    params: GetUsersRequest | None = None,
) -> TwitchResponse[User]:
    """Get information about one or more users.

    If no params provided, returns authenticated user.
    """
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/users", params=query)
    return TwitchResponse[User].model_validate(response)


async def update_user(
    client: "TwitchHTTPClient",
    params: UpdateUserRequest,
) -> TwitchResponse[User]:
    """Update the authenticated user's description."""
    query = params.model_dump(exclude_none=True)
    response = await client.put("/users", params=query)
    return TwitchResponse[User].model_validate(response)


async def get_user_block_list(
    client: "TwitchHTTPClient",
    params: GetUserBlockListRequest,
) -> TwitchResponse[UserBlockTarget]:
    """Get list of users that the broadcaster has blocked."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/users/blocks", params=query)
    return TwitchResponse[UserBlockTarget].model_validate(response)


async def block_user(
    client: "TwitchHTTPClient",
    params: BlockUserRequest,
) -> None:
    """Block a user."""
    query = params.model_dump(exclude_none=True)
    await client.put("/users/blocks", params=query)


async def unblock_user(
    client: "TwitchHTTPClient",
    params: UnblockUserRequest,
) -> None:
    """Unblock a user."""
    query = params.model_dump(exclude_none=True)
    await client.delete("/users/blocks", params=query)


async def get_user_extensions(
    client: "TwitchHTTPClient",
) -> TwitchResponse[UserExtension]:
    """Get list of extensions the authenticated user has installed."""
    response = await client.get("/users/extensions/list")
    return TwitchResponse[UserExtension].model_validate(response)


async def get_user_active_extensions(
    client: "TwitchHTTPClient",
    user_id: str | None = None,
) -> dict:
    """Get user's active extensions."""
    params = {"user_id": user_id} if user_id else {}
    response = await client.get("/users/extensions", params=params)
    return response


async def update_user_extensions(
    client: "TwitchHTTPClient",
    params: UpdateUserExtensionsRequest,
) -> dict:
    """Update user's active extensions."""
    response = await client.put("/users/extensions", data=params.model_dump())
    return response
