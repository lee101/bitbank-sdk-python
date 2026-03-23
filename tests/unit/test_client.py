import pytest
import respx
from httpx import Response

from bitbank import BitbankClient, AuthenticationError, NotFoundError


@pytest.fixture
async def client():
    async with BitbankClient(api_key="test-key", base_url="https://test.bitbank.nz") as c:
        yield c


@respx.mock
async def test_public_summary(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/public-summary").mock(
        return_value=Response(200, json={
            "total_return_pct": 42.5,
            "max_drawdown_pct": -8.2,
            "win_rate_pct": 62.0,
            "trade_count": 150,
            "period_days": 30,
        })
    )
    result = await client.trading_bot.public_summary()
    assert result.total_return_pct == 42.5
    assert result.trade_count == 150


@respx.mock
async def test_signals(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/signals").mock(
        return_value=Response(200, json={
            "signals": [
                {
                    "currency_pair": "BTC_USDT",
                    "timeframe": "hourly",
                    "timestamp": "2025-01-01T00:00:00Z",
                    "buy_price": 95000.0,
                    "sell_price": 96000.0,
                    "confidence": 0.85,
                    "signal_type": "buy",
                    "chronos_median": 95500.0,
                }
            ],
            "timestamp": "2025-01-01T00:00:00Z",
        })
    )
    result = await client.trading_bot.signals()
    assert len(result.signals) == 1
    assert result.signals[0].currency_pair == "BTC_USDT"
    assert result.signals[0].buy_price == 95000.0


@respx.mock
async def test_public_signals_latest(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/public-signals-latest").mock(
        return_value=Response(200, json={
            "signals": [
                {
                    "currency_pair": "ETH_USDT",
                    "timestamp": "2025-01-01T00:00:00Z",
                    "buy_price": 3400.0,
                    "sell_price": 3500.0,
                    "signal_type": "buy",
                    "pnl_7d_pct": 2.5,
                    "trades_7d": 12,
                    "win_rate_7d": 0.67,
                }
            ],
        })
    )
    result = await client.trading_bot.public_signals_latest()
    assert len(result.signals) == 1
    assert result.signals[0].pnl_7d_pct == 2.5


@respx.mock
async def test_fast_forecasts(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/fast-forecasts").mock(
        return_value=Response(200, json={
            "forecasts": [
                {"pair": "BTC_USDT", "ts": "2025-01-01T00:00:00Z", "buy": 95000, "sell": 96000, "signal": "buy", "conf": 0.8}
            ],
            "count": 1,
            "cache_ttl": 5.0,
            "ts": "2025-01-01T00:00:00Z",
        })
    )
    result = await client.trading_bot.fast_forecasts()
    assert result.count == 1
    assert result.forecasts[0].pair == "BTC_USDT"


@respx.mock
async def test_trades_pagination(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/trades").mock(
        return_value=Response(200, json={
            "results": [{"currency_pair": "BTC_USDT", "pnl_pct": 1.5, "pnl_usd": 15.0, "side": "long"}],
            "total": 100,
            "limit": 50,
            "offset": 0,
        })
    )
    result = await client.trading_bot.trades(limit=50, offset=0)
    assert result.total == 100
    assert result.has_next is True
    assert len(result.results) == 1


@respx.mock
async def test_equity_curve(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/equity-curve").mock(
        return_value=Response(200, json={
            "data": [{"timestamp": "2025-01-01T00:00:00Z", "value": 10500, "drawdown_pct": 0, "trade_count": 5, "win_rate": 0.6}],
            "summary": {"total_return_pct": 5.0, "max_drawdown_pct": -2.0, "win_rate": 0.6, "trade_count": 5},
            "initial_equity": 10000,
            "timeframe": "hourly",
        })
    )
    result = await client.trading_bot.equity_curve()
    assert result.initial_equity == 10000
    assert len(result.data) == 1
    assert result.summary.total_return_pct == 5.0


@respx.mock
async def test_forecast_accuracy(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/forecast-accuracy").mock(
        return_value=Response(200, json={
            "lookback_days": 30,
            "as_of": "2025-01-01T00:00:00Z",
            "horizon_1h": {"mae_pct": 0.5, "stdev_pct": 0.3, "samples": 1000},
            "by_pair": [{"pair": "BTC_USDT", "horizon_1h": {"mae_pct": 0.4, "stdev_pct": 0.2, "samples": 500}, "total_samples": 500}],
            "time_series": [],
            "volatility": {},
        })
    )
    result = await client.trading_bot.forecast_accuracy()
    assert result.lookback_days == 30
    assert result.horizon_1h.mae_pct == 0.5
    assert len(result.by_pair) == 1


@respx.mock
async def test_coins(client):
    respx.get("https://test.bitbank.nz/api/coins").mock(
        return_value=Response(200, json={
            "results": [{"currency_pair": "BTC_USDT", "name": "Bitcoin", "symbol": "BTC", "price": 95000}]
        })
    )
    result = await client.forecasts.coins()
    assert len(result) == 1
    assert result[0].currency_pair == "BTC_USDT"


@respx.mock
async def test_forecast_pair(client):
    respx.get("https://test.bitbank.nz/api/forecasts/BTC_USDT").mock(
        return_value=Response(200, json={"currency_pair": "BTC_USDT", "buy_price": 95000, "sell_price": 96000})
    )
    result = await client.forecasts.pair("BTC_USDT")
    assert result.currency_pair == "BTC_USDT"


@respx.mock
async def test_line_forecast(client):
    respx.post("https://test.bitbank.nz/api/forecast/line").mock(
        return_value=Response(200, json={
            "series_length": 100,
            "prediction_length": 24,
            "interval_minutes": 60,
            "forecast": {"low": [1.0] * 24, "median": [2.0] * 24, "high": [3.0] * 24},
            "credits_remaining": 9.5,
        })
    )
    from bitbank.models.forecasts import LineForecastRequest
    req = LineForecastRequest(series=[1.0] * 100, prediction_length=24)
    result = await client.forecasts.line(req)
    assert result.prediction_length == 24
    assert len(result.forecast.median) == 24


@respx.mock
async def test_auth_error(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/signals").mock(
        return_value=Response(401, json={"error": "unauthorized", "message": "Invalid API key"})
    )
    with pytest.raises(AuthenticationError) as exc_info:
        await client.trading_bot.signals()
    assert exc_info.value.status_code == 401


@respx.mock
async def test_not_found_error(client):
    respx.get("https://test.bitbank.nz/api/forecasts/FAKE_PAIR").mock(
        return_value=Response(404, json={"error": "not_found", "message": "Pair not found"})
    )
    with pytest.raises(NotFoundError):
        await client.forecasts.pair("FAKE_PAIR")


@respx.mock
async def test_api_key_header(client):
    route = respx.get("https://test.bitbank.nz/api/trading-bot/signals").mock(
        return_value=Response(200, json={"signals": []})
    )
    await client.trading_bot.signals()
    assert route.calls[0].request.headers["X-API-Key"] == "test-key"


@respx.mock
async def test_signal_spread_pct(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/signals").mock(
        return_value=Response(200, json={
            "signals": [{"currency_pair": "BTC_USDT", "buy_price": 100.0, "sell_price": 101.0}],
        })
    )
    result = await client.trading_bot.signals()
    assert abs(result.signals[0].spread_pct - 0.01) < 1e-6


@respx.mock
async def test_pnl_summary(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/pnl-summary").mock(
        return_value=Response(200, json={
            "total_trades": 200,
            "winning_trades": 120,
            "losing_trades": 80,
            "win_rate": 0.6,
            "total_pnl_pct": 15.5,
            "total_pnl_usd": 1550.0,
        })
    )
    result = await client.trading_bot.pnl_summary()
    assert result.total_trades == 200
    assert result.win_rate == 0.6


@respx.mock
async def test_signal_export(client):
    respx.get("https://test.bitbank.nz/api/trading-bot/signal-export").mock(
        return_value=Response(200, json={
            "days": 30,
            "pairs": ["BTC_USDT", "ETH_USDT"],
            "pair_count": 2,
            "signals": {"BTC_USDT": [{"buy_price": 95000}]},
            "pnl_7d": {},
        })
    )
    result = await client.trading_bot.signal_export(days=30)
    assert result.pair_count == 2
    assert "BTC_USDT" in result.signals
