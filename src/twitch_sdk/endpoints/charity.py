"""Charity endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.charity import (
    CharityCampaign,
    CharityDonation,
    GetCharityCampaignRequest,
    GetCharityDonationsRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_charity_campaign(
    client: "TwitchHTTPClient",
    params: GetCharityCampaignRequest,
) -> TwitchResponse[CharityCampaign]:
    """Get the broadcaster's active charity campaign.

    Requires channel:read:charity scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/charity/campaigns", params=query)
    return TwitchResponse[CharityCampaign].model_validate(response)


async def get_charity_campaign_donations(
    client: "TwitchHTTPClient",
    params: GetCharityDonationsRequest,
) -> TwitchResponse[CharityDonation]:
    """Get donations to the broadcaster's charity campaign.

    Requires channel:read:charity scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/charity/donations", params=query)
    return TwitchResponse[CharityDonation].model_validate(response)
