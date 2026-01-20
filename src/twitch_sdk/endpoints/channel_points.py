"""Channel Points endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.channel_points import (
    CreateCustomRewardRequest,
    CustomReward,
    DeleteCustomRewardRequest,
    GetCustomRewardRedemptionRequest,
    GetCustomRewardsRequest,
    RewardRedemption,
    UpdateCustomRewardRequest,
    UpdateRedemptionStatusRequest,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_custom_rewards(
    client: "TwitchHTTPClient",
    params: GetCustomRewardsRequest,
) -> TwitchResponse[CustomReward]:
    """Get custom rewards for a channel.

    Requires channel:read:redemptions or channel:manage:redemptions scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channel_points/custom_rewards", params=query)
    return TwitchResponse[CustomReward].model_validate(response)


async def create_custom_reward(
    client: "TwitchHTTPClient",
    params: CreateCustomRewardRequest,
) -> TwitchResponse[CustomReward]:
    """Create a custom reward on a channel.

    Requires channel:manage:redemptions scope.
    """
    query = {"broadcaster_id": params.broadcaster_id}
    data = params.model_dump(exclude={"broadcaster_id"}, exclude_none=True)
    response = await client.post("/channel_points/custom_rewards", params=query, data=data)
    return TwitchResponse[CustomReward].model_validate(response)


async def update_custom_reward(
    client: "TwitchHTTPClient",
    params: UpdateCustomRewardRequest,
) -> TwitchResponse[CustomReward]:
    """Update a custom reward on a channel.

    Requires channel:manage:redemptions scope.
    """
    query = {"broadcaster_id": params.broadcaster_id, "id": params.id}
    data = params.model_dump(exclude={"broadcaster_id", "id"}, exclude_none=True)
    response = await client.patch("/channel_points/custom_rewards", params=query, data=data)
    return TwitchResponse[CustomReward].model_validate(response)


async def delete_custom_reward(
    client: "TwitchHTTPClient",
    params: DeleteCustomRewardRequest,
) -> None:
    """Delete a custom reward from a channel.

    Requires channel:manage:redemptions scope.
    """
    query = params.model_dump(exclude_none=True)
    await client.delete("/channel_points/custom_rewards", params=query)


async def get_custom_reward_redemption(
    client: "TwitchHTTPClient",
    params: GetCustomRewardRedemptionRequest,
) -> TwitchResponse[RewardRedemption]:
    """Get redemptions for a custom reward.

    Requires channel:read:redemptions or channel:manage:redemptions scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/channel_points/custom_rewards/redemptions", params=query)
    return TwitchResponse[RewardRedemption].model_validate(response)


async def update_redemption_status(
    client: "TwitchHTTPClient",
    params: UpdateRedemptionStatusRequest,
) -> TwitchResponse[RewardRedemption]:
    """Update the status of a custom reward redemption.

    Requires channel:manage:redemptions scope.
    """
    query = {
        "broadcaster_id": params.broadcaster_id,
        "reward_id": params.reward_id,
        "id": params.id,
    }
    data = {"status": params.status}
    response = await client.patch("/channel_points/custom_rewards/redemptions", params=query, data=data)
    return TwitchResponse[RewardRedemption].model_validate(response)
