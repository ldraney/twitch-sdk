"""Pydantic schemas for Polls endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class PollChoice(TwitchBaseModel):
    """Poll choice data."""

    id: str | None = None  # Optional for edge cases
    title: str
    votes: int = 0
    channel_points_votes: int = 0
    bits_votes: int = 0


class Poll(TwitchBaseModel):
    """Poll data from Twitch API."""

    id: str
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    title: str
    choices: list[PollChoice]
    bits_voting_enabled: bool = False
    bits_per_vote: int = 0
    channel_points_voting_enabled: bool = False
    channel_points_per_vote: int = 0
    status: str  # ACTIVE, COMPLETED, TERMINATED, ARCHIVED, MODERATED, INVALID
    duration: int
    started_at: datetime
    ended_at: datetime | None = None


class PollChoiceInput(TwitchBaseModel):
    """Poll choice for creating a poll."""

    title: str = Field(max_length=25)


class CreatePollRequest(TwitchBaseModel):
    """Request to create a poll."""

    broadcaster_id: str
    title: str = Field(max_length=60)
    choices: list[PollChoiceInput] = Field(min_length=2, max_length=5)
    duration: int = Field(ge=15, le=1800)
    channel_points_voting_enabled: bool = False
    channel_points_per_vote: int = Field(default=0, ge=0, le=1000000)


class GetPollsRequest(TwitchBaseModel):
    """Request params for Get Polls."""

    broadcaster_id: str
    id: list[str] | None = None
    first: int | None = Field(default=None, le=20)
    after: str | None = None


class EndPollRequest(TwitchBaseModel):
    """Request to end a poll."""

    broadcaster_id: str
    id: str
    status: str  # TERMINATED or ARCHIVED
