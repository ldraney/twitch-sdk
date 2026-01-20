"""Pydantic schemas for Whispers endpoints."""

from pydantic import Field

from .base import TwitchBaseModel


class SendWhisperRequest(TwitchBaseModel):
    """Request to send a whisper."""

    from_user_id: str
    to_user_id: str
    message: str = Field(max_length=10000)
