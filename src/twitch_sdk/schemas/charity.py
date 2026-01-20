"""Pydantic schemas for Charity endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class CharityAmount(TwitchBaseModel):
    """Charity amount with currency."""

    value: int
    decimal_places: int
    currency: str


class CharityCampaign(TwitchBaseModel):
    """Charity campaign data."""

    id: str
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    charity_name: str
    charity_description: str
    charity_logo: str
    charity_website: str
    current_amount: CharityAmount
    target_amount: CharityAmount


class GetCharityCampaignRequest(TwitchBaseModel):
    """Request params for Get Charity Campaign."""

    broadcaster_id: str


class CharityDonation(TwitchBaseModel):
    """Charity donation data."""

    id: str
    campaign_id: str
    user_id: str
    user_login: str
    user_name: str
    amount: CharityAmount


class GetCharityDonationsRequest(TwitchBaseModel):
    """Request params for Get Charity Campaign Donations."""

    broadcaster_id: str
    first: int | None = Field(default=None, le=100)
    after: str | None = None
