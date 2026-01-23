"""Pydantic schemas for Bits endpoints."""

from datetime import datetime

from pydantic import Field

from .base import DateRange, TwitchBaseModel


class BitsLeaderboardEntry(TwitchBaseModel):
    """Entry in the bits leaderboard."""

    user_id: str
    user_login: str
    user_name: str
    rank: int
    score: int


class GetBitsLeaderboardRequest(TwitchBaseModel):
    """Request params for Get Bits Leaderboard."""

    count: int | None = Field(default=None, le=100)
    period: str | None = None  # day, week, month, year, all
    started_at: datetime | None = None
    user_id: str | None = None


class GetBitsLeaderboardResponse(TwitchBaseModel):
    """Response from Get Bits Leaderboard."""

    data: list[BitsLeaderboardEntry]
    date_range: DateRange
    total: int


class CheermoteTier(TwitchBaseModel):
    """Cheermote tier data."""

    min_bits: int
    id: str
    color: str
    # images structure: {"dark": {"animated": {"1": url, "2": url, ...}, "static": {...}}, "light": {...}}
    images: dict[str, dict[str, dict[str, str]]]
    can_cheer: bool
    show_in_bits_card: bool


class Cheermote(TwitchBaseModel):
    """Cheermote data."""

    prefix: str
    tiers: list[CheermoteTier]
    type: str
    order: int
    last_updated: datetime
    is_charitable: bool


class GetCheermotesRequest(TwitchBaseModel):
    """Request params for Get Cheermotes."""

    broadcaster_id: str | None = None


class ExtensionTransaction(TwitchBaseModel):
    """Extension transaction data."""

    id: str
    timestamp: datetime
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    user_id: str
    user_login: str
    user_name: str
    product_type: str
    product_data: dict


class GetExtensionTransactionsRequest(TwitchBaseModel):
    """Request params for Get Extension Transactions."""

    extension_id: str
    id: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None
