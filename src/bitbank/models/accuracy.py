from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["ErrorSummary", "PairAccuracy", "DailyAccuracy", "ForecastAccuracy"]


class ErrorSummary(BaseModel):
    mae_pct: float | None = None
    stdev_pct: float | None = None
    samples: int = 0


class PairAccuracy(BaseModel):
    pair: str = ""
    horizon_1h: ErrorSummary | None = None
    horizon_1d: ErrorSummary | None = None
    total_samples: int = 0
    model_config = {"extra": "allow"}


class DailyAccuracy(BaseModel):
    date: str = ""
    horizon_1h: ErrorSummary | None = None
    total_samples: int = 0
    model_config = {"extra": "allow"}


class ForecastAccuracy(BaseModel):
    lookback_days: int = 0
    as_of: str | None = None
    source: str | None = None
    horizon_1h: ErrorSummary | None = None
    horizon_1d: ErrorSummary | None = None
    by_pair: list[PairAccuracy] = Field(default_factory=list)
    time_series: list[DailyAccuracy] = Field(default_factory=list)
    volatility: dict = Field(default_factory=dict)
    model_config = {"extra": "allow"}
