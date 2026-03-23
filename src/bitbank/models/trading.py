from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "PublicSummary",
    "PublicPerformance",
    "PairPerformance",
    "Trade",
    "TradesResponse",
    "PnlSummary",
    "EquityPoint",
    "EquitySummary",
    "EquityCurveResponse",
]


class PublicSummary(BaseModel):
    total_return_pct: float | None = None
    max_drawdown_pct: float | None = None
    win_rate_pct: float | None = None
    trade_count: int = 0
    period_days: int = 0


class PairPerformance(BaseModel):
    pair: str = ""
    total_return_pct: float = 0.0
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    trade_count: int = 0
    win_rate_pct: float | None = None


class PublicPerformance(BaseModel):
    total_return_pct: float | None = None
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    max_drawdown_pct: float | None = None
    win_rate_pct: float | None = None
    trade_count: int = 0
    period_days: int = 0
    pairs: list[PairPerformance] = Field(default_factory=list)


class Trade(BaseModel):
    id: int | None = None
    currency_pair: str = ""
    timeframe: str | None = None
    side: str = ""
    entry_price: float = 0.0
    exit_price: float = 0.0
    entry_timestamp: str | None = None
    exit_timestamp: str | None = None
    position_size_pct: float | None = None
    pnl_pct: float = 0.0
    pnl_usd: float = 0.0
    fees_pct: float = 0.0
    model_config = {"extra": "allow"}


class TradesResponse(BaseModel):
    results: list[Trade] = Field(default_factory=list)
    total: int = 0
    limit: int = 50
    offset: int = 0

    @property
    def has_next(self) -> bool:
        return self.offset + self.limit < self.total


class PnlSummary(BaseModel):
    model_config = {"extra": "allow"}
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl_pct: float = 0.0
    total_pnl_usd: float = 0.0
    avg_win_pct: float = 0.0
    avg_loss_pct: float = 0.0
    best_trade_pct: float = 0.0
    worst_trade_pct: float = 0.0


class EquityPoint(BaseModel):
    timestamp: str = ""
    value: float = 0.0
    drawdown_pct: float = 0.0
    trade_count: int = 0
    win_rate: float = 0.0
    model_config = {"extra": "allow"}


class EquitySummary(BaseModel):
    total_return_pct: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate: float = 0.0
    trade_count: int = 0
    model_config = {"extra": "allow"}


class EquityCurveResponse(BaseModel):
    data: list[EquityPoint] = Field(default_factory=list)
    summary: EquitySummary | None = None
    initial_equity: float = 0.0
    pair: str | None = None
    timeframe: str = "hourly"
    trades: list[Trade] | None = None
    model_config = {"extra": "allow"}
