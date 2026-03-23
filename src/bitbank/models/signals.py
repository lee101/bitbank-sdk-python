from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "Signal",
    "SignalsResponse",
    "PublicSignalLatest",
    "PublicSignalsLatestResponse",
    "FastForecast",
    "FastForecastsResponse",
    "SignalExportResponse",
    "SignalHistoryResponse",
    "WebhookInfo",
]


class Signal(BaseModel):
    id: int | None = None
    currency_pair: str
    timeframe: str = "hourly"
    timestamp: str | None = None
    buy_price: float
    sell_price: float
    trade_amount_pct: float | None = None
    confidence: float | None = None
    signal_type: str = "hold"
    chronos_low: float | None = None
    chronos_median: float | None = None
    chronos_high: float | None = None
    model_type: str | None = None

    @property
    def spread_pct(self) -> float:
        if self.buy_price <= 0:
            return 0.0
        return (self.sell_price - self.buy_price) / self.buy_price


class SignalsResponse(BaseModel):
    signals: list[Signal] = Field(default_factory=list)
    timestamp: str | None = None


class PublicSignalLatest(BaseModel):
    currency_pair: str = ""
    timestamp: str | None = None
    buy_price: float = 0.0
    sell_price: float = 0.0
    signal_type: str = "hold"
    confidence: float | None = None
    pnl_7d_pct: float = 0.0
    trades_7d: int = 0
    win_rate_7d: float | None = None


class PublicSignalsLatestResponse(BaseModel):
    signals: list[PublicSignalLatest] = Field(default_factory=list)
    timestamp: str | None = None


class FastForecast(BaseModel):
    pair: str
    ts: str
    buy: float
    sell: float
    signal: str
    conf: float | None = None


class FastForecastsResponse(BaseModel):
    forecasts: list[FastForecast] = Field(default_factory=list)
    count: int = 0
    cache_ttl: float = 5.0
    ts: str | None = None


class SignalExportResponse(BaseModel):
    days: int = 60
    pairs: list[str] = Field(default_factory=list)
    pair_count: int = 0
    signals: dict = Field(default_factory=dict)
    pnl_7d: dict = Field(default_factory=dict)
    timestamp: str | None = None


class SignalHistoryResponse(BaseModel):
    signals: list[dict] = Field(default_factory=list)
    pair: str = ""
    count: int = 0


class WebhookInfo(BaseModel):
    model_config = {"extra": "allow"}
