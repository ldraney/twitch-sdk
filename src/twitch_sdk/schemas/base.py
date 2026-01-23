"""Base schemas used across endpoints."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, field_validator

T = TypeVar("T")


class TwitchBaseModel(BaseModel):
    """Base model for all Twitch schemas."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",  # Ignore unknown fields from API
    )


class Pagination(TwitchBaseModel):
    """Pagination info in API responses."""

    cursor: str | None = None


class TwitchResponse(TwitchBaseModel, Generic[T]):
    """Generic wrapper for Twitch API responses with data array."""

    data: list[T]
    pagination: Pagination | None = None
    total: int | None = None


class DateRange(TwitchBaseModel):
    """Date range for analytics."""

    started_at: datetime | None = None
    ended_at: datetime | None = None

    @field_validator("started_at", "ended_at", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Convert empty strings to None for optional datetime fields."""
        if v == "":
            return None
        return v
