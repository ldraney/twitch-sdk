"""Pydantic schemas for Channels endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class Channel(TwitchBaseModel):
    """Channel information."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    broadcaster_language: str
    game_id: str
    game_name: str
    title: str
    delay: int
    tags: list[str] = Field(default_factory=list)
    content_classification_labels: list[str] = Field(default_factory=list)
    is_branded_content: bool


class GetChannelInfoRequest(TwitchBaseModel):
    """Request params for Get Channel Information."""

    broadcaster_id: list[str]


class ModifyChannelInfoRequest(TwitchBaseModel):
    """Request to modify channel information."""

    broadcaster_id: str
    game_id: str | None = None
    broadcaster_language: str | None = None
    title: str | None = None
    delay: int | None = None
    tags: list[str] | None = None
    content_classification_labels: list[dict] | None = None
    is_branded_content: bool | None = None


class ChannelEditor(TwitchBaseModel):
    """Channel editor info."""

    user_id: str
    user_name: str
    created_at: datetime


class GetChannelEditorsRequest(TwitchBaseModel):
    """Request params for Get Channel Editors."""

    broadcaster_id: str


class FollowedChannel(TwitchBaseModel):
    """Channel that a user follows."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    followed_at: datetime


class GetFollowedChannelsRequest(TwitchBaseModel):
    """Request params for Get Followed Channels."""

    user_id: str
    broadcaster_id: str | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class Follower(TwitchBaseModel):
    """Channel follower info."""

    user_id: str
    user_login: str
    user_name: str
    followed_at: datetime


class GetChannelFollowersRequest(TwitchBaseModel):
    """Request params for Get Channel Followers."""

    broadcaster_id: str
    user_id: str | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class GetChannelFollowersResponse(TwitchBaseModel):
    """Response from Get Channel Followers."""

    data: list[Follower]
    pagination: dict | None = None
    total: int


class VIP(TwitchBaseModel):
    """VIP user info."""

    user_id: str
    user_login: str
    user_name: str


class GetVIPsRequest(TwitchBaseModel):
    """Request params for Get VIPs."""

    broadcaster_id: str
    user_id: list[str] | None = None
    first: int | None = Field(default=None, le=100)
    after: str | None = None


class AddVIPRequest(TwitchBaseModel):
    """Request to add a VIP."""

    broadcaster_id: str
    user_id: str


class RemoveVIPRequest(TwitchBaseModel):
    """Request to remove a VIP."""

    broadcaster_id: str
    user_id: str
