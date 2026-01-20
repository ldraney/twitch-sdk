"""Subscriptions endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.subscriptions import (
    CheckUserSubscriptionRequest,
    GetBroadcasterSubscriptionsRequest,
    GetBroadcasterSubscriptionsResponse,
    UserSubscription,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_broadcaster_subscriptions(
    client: "TwitchHTTPClient",
    params: GetBroadcasterSubscriptionsRequest,
) -> GetBroadcasterSubscriptionsResponse:
    """Get list of subscribers for a broadcaster.

    Requires channel:read:subscriptions scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/subscriptions", params=query)
    return GetBroadcasterSubscriptionsResponse.model_validate(response)


async def check_user_subscription(
    client: "TwitchHTTPClient",
    params: CheckUserSubscriptionRequest,
) -> TwitchResponse[UserSubscription]:
    """Check if a user is subscribed to a broadcaster.

    Requires user:read:subscriptions scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/subscriptions/user", params=query)
    return TwitchResponse[UserSubscription].model_validate(response)
