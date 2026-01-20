"""Pydantic schemas for Schedule endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class ScheduleCategory(TwitchBaseModel):
    """Category for a scheduled segment."""

    id: str
    name: str


class ScheduleSegment(TwitchBaseModel):
    """Scheduled stream segment."""

    id: str
    start_time: datetime
    end_time: datetime
    title: str
    canceled_until: datetime | None = None
    category: ScheduleCategory | None = None
    is_recurring: bool


class ScheduleVacation(TwitchBaseModel):
    """Vacation period in schedule."""

    start_time: datetime
    end_time: datetime


class Schedule(TwitchBaseModel):
    """Channel schedule."""

    segments: list[ScheduleSegment] | None = None
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    vacation: ScheduleVacation | None = None


class GetScheduleRequest(TwitchBaseModel):
    """Request params for Get Channel Stream Schedule."""

    broadcaster_id: str
    id: list[str] | None = None
    start_time: datetime | None = None
    utc_offset: str | None = None
    first: int | None = Field(default=None, le=25)
    after: str | None = None


class GetScheduleICalendarRequest(TwitchBaseModel):
    """Request params for Get Channel iCalendar."""

    broadcaster_id: str


class UpdateScheduleRequest(TwitchBaseModel):
    """Request to update channel schedule settings."""

    broadcaster_id: str
    is_vacation_enabled: bool | None = None
    vacation_start_time: datetime | None = None
    vacation_end_time: datetime | None = None
    timezone: str | None = None


class CreateScheduleSegmentRequest(TwitchBaseModel):
    """Request to create a schedule segment."""

    broadcaster_id: str
    start_time: datetime
    timezone: str
    duration: int = Field(ge=30, le=1440)  # minutes
    is_recurring: bool = False
    category_id: str | None = None
    title: str | None = Field(default=None, max_length=140)


class UpdateScheduleSegmentRequest(TwitchBaseModel):
    """Request to update a schedule segment."""

    broadcaster_id: str
    id: str
    start_time: datetime | None = None
    timezone: str | None = None
    duration: int | None = Field(default=None, ge=30, le=1440)
    is_canceled: bool | None = None
    category_id: str | None = None
    title: str | None = Field(default=None, max_length=140)


class DeleteScheduleSegmentRequest(TwitchBaseModel):
    """Request to delete a schedule segment."""

    broadcaster_id: str
    id: str
