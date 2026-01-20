"""Predictions endpoints."""

from typing import TYPE_CHECKING

from twitch_sdk.schemas.base import TwitchResponse
from twitch_sdk.schemas.predictions import (
    CreatePredictionRequest,
    EndPredictionRequest,
    GetPredictionsRequest,
    Prediction,
)

if TYPE_CHECKING:
    from twitch_client import TwitchHTTPClient


async def get_predictions(
    client: "TwitchHTTPClient",
    params: GetPredictionsRequest,
) -> TwitchResponse[Prediction]:
    """Get predictions for a channel.

    Requires channel:read:predictions scope.
    """
    query = params.model_dump(exclude_none=True)
    response = await client.get("/predictions", params=query)
    return TwitchResponse[Prediction].model_validate(response)


async def create_prediction(
    client: "TwitchHTTPClient",
    params: CreatePredictionRequest,
) -> TwitchResponse[Prediction]:
    """Create a prediction on a channel.

    Requires channel:manage:predictions scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.post("/predictions", data=data)
    return TwitchResponse[Prediction].model_validate(response)


async def end_prediction(
    client: "TwitchHTTPClient",
    params: EndPredictionRequest,
) -> TwitchResponse[Prediction]:
    """End an active prediction.

    Requires channel:manage:predictions scope.
    """
    data = params.model_dump(exclude_none=True)
    response = await client.patch("/predictions", data=data)
    return TwitchResponse[Prediction].model_validate(response)
