from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bitbank.models.signals import (
    FastForecastsResponse,
    PublicSignalsLatestResponse,
    SignalExportResponse,
    SignalHistoryResponse,
    SignalsResponse,
    WebhookInfo,
)
from bitbank.models.trading import (
    EquityCurveResponse,
    PnlSummary,
    PublicPerformance,
    PublicSummary,
    TradesResponse,
)
from bitbank.models.accuracy import ForecastAccuracy

if TYPE_CHECKING:
    from bitbank._http import HttpTransport


class TradingBotEndpoints:
    def __init__(self, http: HttpTransport):
        self._http = http

    async def signals(self) -> SignalsResponse:
        data = await self._http.get("/api/trading-bot/signals")
        return SignalsResponse.model_validate(data)

    async def signal(self, pair: str) -> SignalsResponse:
        data = await self._http.get(f"/api/trading-bot/signals/{pair}")
        return SignalsResponse.model_validate(data)

    async def equity_curve(self, pair: str | None = None, include_trades: bool = False) -> EquityCurveResponse:
        params: dict[str, Any] = {}
        if pair:
            params["pair"] = pair
        if include_trades:
            params["include_trades"] = "true"
        data = await self._http.get("/api/trading-bot/equity-curve", params=params)
        return EquityCurveResponse.model_validate(data)

    async def trades(self, limit: int = 50, offset: int = 0, pair: str | None = None) -> TradesResponse:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if pair:
            params["pair"] = pair
        data = await self._http.get("/api/trading-bot/trades", params=params)
        return TradesResponse.model_validate(data)

    async def pnl_summary(self) -> PnlSummary:
        data = await self._http.get("/api/trading-bot/pnl-summary")
        return PnlSummary.model_validate(data)

    async def pairs(self) -> list[str]:
        data = await self._http.get("/api/trading-bot/pairs")
        return data.get("pairs", data if isinstance(data, list) else [])

    async def public_summary(self) -> PublicSummary:
        data = await self._http.get("/api/trading-bot/public-summary")
        return PublicSummary.model_validate(data)

    async def public_performance(self) -> PublicPerformance:
        data = await self._http.get("/api/trading-bot/public-performance")
        return PublicPerformance.model_validate(data)

    async def forecast_accuracy(self, lookback_days: int | None = None) -> ForecastAccuracy:
        params: dict[str, Any] = {}
        if lookback_days is not None:
            params["lookback_days"] = lookback_days
        data = await self._http.get("/api/trading-bot/forecast-accuracy", params=params)
        return ForecastAccuracy.model_validate(data)

    async def public_signals_history(self, pair: str, days: int | None = None) -> SignalHistoryResponse:
        params: dict[str, Any] = {"pair": pair}
        if days is not None:
            params["days"] = days
        data = await self._http.get("/api/trading-bot/public-signals-history", params=params)
        return SignalHistoryResponse.model_validate(data)

    async def signal_export(self, days: int = 60) -> SignalExportResponse:
        data = await self._http.get("/api/trading-bot/signal-export", params={"days": days})
        return SignalExportResponse.model_validate(data)

    async def public_signals_latest(self) -> PublicSignalsLatestResponse:
        data = await self._http.get("/api/trading-bot/public-signals-latest")
        return PublicSignalsLatestResponse.model_validate(data)

    async def fast_forecasts(self) -> FastForecastsResponse:
        data = await self._http.get("/api/trading-bot/fast-forecasts")
        return FastForecastsResponse.model_validate(data)

    async def webhook_info(self) -> WebhookInfo:
        data = await self._http.get("/api/trading-bot/webhook-info")
        return WebhookInfo.model_validate(data)
