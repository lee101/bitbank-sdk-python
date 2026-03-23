import os
import pytest
from bitbank import BitbankClient

pytestmark = pytest.mark.integration
BASE_URL = os.getenv("BITBANK_BASE_URL", "https://bitbank.nz")


@pytest.fixture
async def client():
    async with BitbankClient(base_url=BASE_URL) as c:
        yield c


async def test_public_summary(client):
    result = await client.trading_bot.public_summary()
    assert result.period_days > 0


async def test_public_performance(client):
    result = await client.trading_bot.public_performance()
    assert result.trade_count >= 0


async def test_forecast_accuracy(client):
    result = await client.trading_bot.forecast_accuracy()
    assert result.lookback_days > 0


async def test_public_signals_latest(client):
    result = await client.trading_bot.public_signals_latest()
    assert len(result.signals) > 0


async def test_fast_forecasts(client):
    result = await client.trading_bot.fast_forecasts()
    assert result.count > 0


async def test_signal_export(client):
    result = await client.trading_bot.signal_export(days=7)
    assert result.pair_count > 0


async def test_coins(client):
    coins = await client.forecasts.coins()
    assert len(coins) > 0


async def test_hourly_forecasts(client):
    forecasts = await client.forecasts.hourly()
    assert len(forecasts) >= 0
