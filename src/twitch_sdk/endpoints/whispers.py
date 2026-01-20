"""Whispers endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.whispers import SendWhisperRequest

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def send_whisper(
    client: "TwitchHTTPClient",
    params: SendWhisperRequest,
) -> None:
    """Send a whisper to another user.

    Requires user:manage:whispers scope.
    """
    query = {"from_user_id": params.from_user_id, "to_user_id": params.to_user_id}
    data = {"message": params.message}
    await client.post("/whispers", params=query, data=data)
