"""Bits endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.bits import (
    Cheermote,
    ExtensionTransaction,
    GetBitsLeaderboardRequest,
    GetBitsLeaderboardResponse,
    GetCheermotesRequest,
    GetExtensionTransactionsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_bits_leaderboard(
    client: "TwitchHTTPClient",
    params: GetBitsLeaderboardRequest | None = None,
) -> GetBitsLeaderboardResponse:
    """Get bits leaderboard for a channel.

    Requires bits:read scope.
    """
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/bits/leaderboard", params=query)
    return GetBitsLeaderboardResponse.model_validate(response)


async def get_cheermotes(
    client: "TwitchHTTPClient",
    params: GetCheermotesRequest | None = None,
) -> TwitchResponse[Cheermote]:
    """Get cheermotes for a channel or global cheermotes."""
    query = params.model_dump(exclude_none=True) if params else {}
    response = await client.get("/bits/cheermotes", params=query)
    return TwitchResponse[Cheermote].model_validate(response)


async def get_extension_transactions(
    client: "TwitchHTTPClient",
    params: GetExtensionTransactionsRequest,
) -> TwitchResponse[ExtensionTransaction]:
    """Get extension transactions.

    Requires extension developer or extension owner.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/extensions/transactions", params=query)
    return TwitchResponse[ExtensionTransaction].model_validate(response)
