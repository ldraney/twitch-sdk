"""Pydantic schemas for Predictions endpoints."""

from datetime import datetime

from pydantic import Field

from .base import TwitchBaseModel


class TopPredictor(TwitchBaseModel):
    """Top predictor info."""

    user_id: str
    user_login: str
    user_name: str
    channel_points_used: int
    channel_points_won: int


class PredictionOutcome(TwitchBaseModel):
    """Prediction outcome data."""

    id: str
    title: str
    users: int = 0
    channel_points: int = 0
    top_predictors: list[TopPredictor] | None = None
    color: str  # BLUE, PINK


class Prediction(TwitchBaseModel):
    """Prediction data from Twitch API."""

    id: str
    broadcaster_id: str
    broadcaster_login: str
    broadcaster_name: str
    title: str
    winning_outcome_id: str | None = None
    outcomes: list[PredictionOutcome]
    prediction_window: int
    status: str  # ACTIVE, RESOLVED, CANCELED, LOCKED
    created_at: datetime
    ended_at: datetime | None = None
    locked_at: datetime | None = None


class PredictionOutcomeInput(TwitchBaseModel):
    """Prediction outcome for creating a prediction."""

    title: str = Field(max_length=25)


class CreatePredictionRequest(TwitchBaseModel):
    """Request to create a prediction."""

    broadcaster_id: str
    title: str = Field(max_length=45)
    outcomes: list[PredictionOutcomeInput] = Field(min_length=2, max_length=10)
    prediction_window: int = Field(ge=30, le=1800)


class GetPredictionsRequest(TwitchBaseModel):
    """Request params for Get Predictions."""

    broadcaster_id: str
    id: list[str] | None = None
    first: int | None = Field(default=None, le=25)
    after: str | None = None


class EndPredictionRequest(TwitchBaseModel):
    """Request to end a prediction."""

    broadcaster_id: str
    id: str
    status: str  # RESOLVED, CANCELED, LOCKED
    winning_outcome_id: str | None = None  # Required if RESOLVED
