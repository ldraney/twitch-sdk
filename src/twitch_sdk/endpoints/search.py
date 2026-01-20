"""Search endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.search import (
    SearchCategoriesRequest,
    SearchCategory,
    SearchChannel,
    SearchChannelsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def search_categories(
    client: "TwitchHTTPClient",
    params: SearchCategoriesRequest,
) -> TwitchResponse[SearchCategory]:
    """Search for categories/games."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/search/categories", params=query)
    return TwitchResponse[SearchCategory].model_validate(response)


async def search_channels(
    client: "TwitchHTTPClient",
    params: SearchChannelsRequest,
) -> TwitchResponse[SearchChannel]:
    """Search for channels."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/search/channels", params=query)
    return TwitchResponse[SearchChannel].model_validate(response)
