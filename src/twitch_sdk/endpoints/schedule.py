"""Schedule endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.schedule import (
    CreateScheduleSegmentRequest,
    DeleteScheduleSegmentRequest,
    GetScheduleICalendarRequest,
    GetScheduleRequest,
    Schedule,
    ScheduleSegment,
    UpdateScheduleRequest,
    UpdateScheduleSegmentRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_channel_stream_schedule(
    client: "TwitchHTTPClient",
    params: GetScheduleRequest,
) -> dict:
    """Get a broadcaster's streaming schedule."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/schedule", params=query)
    return response


async def get_channel_icalendar(
    client: "TwitchHTTPClient",
    params: GetScheduleICalendarRequest,
) -> str:
    """Get a broadcaster's schedule as iCalendar data."""
    query = params.model_dump(exclude_none=True)
    response = await client.get("/schedule/icalendar", params=query)
    return response


async def update_channel_stream_schedule(
    client: "TwitchHTTPClient",
    params: UpdateScheduleRequest,
) -> None:
    """Update a broadcaster's streaming schedule settings.

    Requires channel:manage:schedule scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.patch("/schedule/settings", params=query)


async def create_channel_stream_schedule_segment(
    client: "TwitchHTTPClient",
    params: CreateScheduleSegmentRequest,
) -> dict:
    """Create a scheduled broadcast segment.

    Requires channel:manage:schedule scope.
    """
    query = {"broadcaster_id": params.broadcaster_id}
    data = params.model_dump(exclude={"broadcaster_id"}, exclude_none=True)
    response = await client.post("/schedule/segment", params=query, data=data)
    return response


async def update_channel_stream_schedule_segment(
    client: "TwitchHTTPClient",
    params: UpdateScheduleSegmentRequest,
) -> dict:
    """Update a scheduled broadcast segment.

    Requires channel:manage:schedule scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "id": params.id}
    data = params.model_dump(exclude={"broadcaster_id", "id"}, exclude_none=True)
    response = await client.patch("/schedule/segment", params=query, data=data)
    return response


async def delete_channel_stream_schedule_segment(
    client: "TwitchHTTPClient",
    params: DeleteScheduleSegmentRequest,
) -> None:
    """Delete a scheduled broadcast segment.

    Requires channel:manage:schedule scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/schedule/segment", params=query)
