"""Pydantic schemas for Channel Points endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class CustomRewardImage(TwitchBaseModel):
    """Custom reward image URLs."""

    url_1x: str
    url_2x: str
    url_4x: str


class MaxPerStreamSetting(TwitchBaseModel):
    """Max per stream setting."""

    is_enabled: bool
    max_per_stream: int


class MaxPerUserPerStreamSetting(TwitchBaseModel):
    """Max per user per stream setting."""

    is_enabled: bool
    max_per_user_per_stream: int


class GlobalCooldownSetting(TwitchBaseModel):
    """Global cooldown setting."""

    is_enabled: bool
    global_cooldown_seconds: int


class CustomReward(TwitchBaseModel):
    """Custom channel points reward."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    id: str
    title: str
    prompt: str
    cost: int
    image: CustomRewardImage | None = None
    default_image: CustomRewardImage
    background_color: str
    is_enabled: bool
    is_user_input_required: bool
    max_per_stream_setting: MaxPerStreamSetting
    max_per_user_per_stream_setting: MaxPerUserPerStreamSetting
    global_cooldown_setting: GlobalCooldownSetting
    is_paused: bool
    is_in_stock: bool
    should_redemptions_skip_request_queue: bool
    redemptions_redeemed_current_stream: int | None = None
    cooldown_expires_at: datetime | None = None


class GetCustomRewardsRequest(TwitchBaseModel):
    """Request params for Get Custom Reward."""

    broadcaster_id: str
    id: list[str] | None = None
    only_manageable_rewards: bool = False


class CreateCustomRewardRequest(TwitchBaseModel):
    """Request to create a custom reward."""

    broadcaster_id: str
    title: str = Field(max_length=45)
    cost: int = Field(ge=1)
    prompt: str | None = Field(default=None, max_length=200)
    is_enabled: bool = True
    background_color: str | None = None
    is_user_input_required: bool = False
    is_max_per_stream_enabled: bool = False
    max_per_stream: int | None = None
    is_max_per_user_per_stream_enabled: bool = False
    max_per_user_per_stream: int | None = None
    is_global_cooldown_enabled: bool = False
    global_cooldown_seconds: int | None = None
    should_redemptions_skip_request_queue: bool = False


class UpdateCustomRewardRequest(TwitchBaseModel):
    """Request to update a custom reward."""

    broadcaster_id: str
    id: str
    title: str | None = Field(default=None, max_length=45)
    cost: int | None = Field(default=None, ge=1)
    prompt: str | None = Field(default=None, max_length=200)
    is_enabled: bool | None = None
    background_color: str | None = None
    is_user_input_required: bool | None = None
    is_max_per_stream_enabled: bool | None = None
    max_per_stream: int | None = None
    is_max_per_user_per_stream_enabled: bool | None = None
    max_per_user_per_stream: int | None = None
    is_global_cooldown_enabled: bool | None = None
    global_cooldown_seconds: int | None = None
    should_redemptions_skip_request_queue: bool | None = None
    is_paused: bool | None = None


class DeleteCustomRewardRequest(TwitchBaseModel):
    """Request to delete a custom reward."""

    broadcaster_id: str
    id: str


class RewardRedemption(TwitchBaseModel):
    """Channel points reward redemption."""

    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    id: str
    user_id: str
    user_login: str
    user_name: str
    user_input: str
    status: str  # CANCELED, FULFILLED, UNFULFILLED
    redeemed_at: datetime
    reward: dict


class GetCustomRewardRedemptionRequest(TwitchBaseModel):
    """Request params for Get Custom Reward Redemption."""

    broadcaster_id: str
    reward_id: str
    id: list[str] | None = None
    status: str | None = None  # CANCELED, FULFILLED, UNFULFILLED
    sort: str | None = None  # OLDEST, NEWEST
    first: int | None = Field(default=None, le=50)
    after: str | None = None


class UpdateRedemptionStatusRequest(TwitchBaseModel):
    """Request to update redemption status."""

    broadcaster_id: str
    reward_id: str
    id: list[str]
    status: str  # CANCELED, FULFILLED
