from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "Forecast",
    "ForecastBar",
    "ForecastBarsResponse",
    "HourlyForecast",
    "DailyForecastResponse",
    "HomepageForecastResponse",
    "LineForecastRequest",
    "LineForecastValues",
    "LineForecastResult",
]


class Forecast(BaseModel):
    model_config = {"extra": "allow"}
    currency_pair: str = ""
    timestamp: str | None = None
    buy_price: float | None = None
    sell_price: float | None = None
    signal_type: str | None = None
    confidence: float | None = None
    chronos_low: float | None = None
    chronos_median: float | None = None
    chronos_high: float | None = None


class ForecastBar(BaseModel):
    model_config = {"extra": "allow"}
    timestamp: str = ""
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None


class ForecastBarsResponse(BaseModel):
    bars: list[ForecastBar] = Field(default_factory=list)
    pair: str = ""
    model_config = {"extra": "allow"}


class HourlyForecast(BaseModel):
    model_config = {"extra": "allow"}


class DailyForecastResponse(BaseModel):
    model_config = {"extra": "allow"}


class HomepageForecastResponse(BaseModel):
    model_config = {"extra": "allow"}


class LineForecastRequest(BaseModel):
    series: list[float]
    prediction_length: int = 24
    interval_minutes: int = 60


class LineForecastValues(BaseModel):
    low: list[float] = Field(default_factory=list)
    median: list[float] = Field(default_factory=list)
    high: list[float] = Field(default_factory=list)


class LineForecastResult(BaseModel):
    series_length: int = 0
    prediction_length: int = 0
    interval_minutes: int = 0
    forecast: LineForecastValues = Field(default_factory=LineForecastValues)
    engine: str | None = None
    generated_at: str | None = None
    credits_used: float = 0.0
    credits_remaining: float = 0.0
    forecast_timestamps: list[str] | None = None
