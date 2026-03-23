from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bitbank.models.forecasts import (
    DailyForecastResponse,
    Forecast,
    ForecastBarsResponse,
    HomepageForecastResponse,
    LineForecastRequest,
    LineForecastResult,
)
from bitbank.models.coins import Coin

if TYPE_CHECKING:
    from bitbank._http import HttpTransport


class ForecastEndpoints:
    def __init__(self, http: HttpTransport):
        self._http = http

    async def coins(self) -> list[Coin]:
        data = await self._http.get("/api/coins")
        items = data.get("results", data if isinstance(data, list) else [])
        return [Coin.model_validate(c) for c in items]

    async def hourly(self) -> list[Forecast]:
        data = await self._http.get("/api/coins/forecasts/hourly")
        items = data if isinstance(data, list) else data.get("forecasts", [])
        return [Forecast.model_validate(f) for f in items]

    async def hourly_pair(self, pair: str) -> Forecast:
        data = await self._http.get(f"/api/coins/forecasts/hourly/{pair}")
        return Forecast.model_validate(data)

    async def all(self) -> dict[str, Any]:
        return await self._http.get("/api/forecasts")

    async def pair(self, pair: str) -> Forecast:
        data = await self._http.get(f"/api/forecasts/{pair}")
        return Forecast.model_validate(data)

    async def bars(self, pair: str, steps: int = 7) -> ForecastBarsResponse:
        data = await self._http.get(f"/api/forecasts/{pair}/bars", params={"steps": steps})
        return ForecastBarsResponse.model_validate(data)

    async def homepage(self, pair: str) -> HomepageForecastResponse:
        data = await self._http.get(f"/api/homepage/forecast/{pair}")
        return HomepageForecastResponse.model_validate(data)

    async def daily(self, pair: str) -> DailyForecastResponse:
        data = await self._http.get(f"/api/forecast/daily/{pair}")
        return DailyForecastResponse.model_validate(data)

    async def line(self, request: LineForecastRequest) -> LineForecastResult:
        data = await self._http.post("/api/forecast/line", json=request.model_dump())
        return LineForecastResult.model_validate(data)
