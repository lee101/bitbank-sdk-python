# bitbank-sdk-python

Python SDK for the [bitbank.nz](https://bitbank.nz) cryptocurrency trading API. Get forecasts, trading signals, performance data, and execute account operations.

## Install

```bash
pip install bitbank-sdk
```

## Quick Start

```python
import asyncio
from bitbank import BitbankClient

async def main():
    async with BitbankClient() as client:
        # Public endpoints (no API key needed)
        signals = await client.trading_bot.public_signals_latest()
        for s in signals.signals:
            print(f"{s.currency_pair}: buy={s.buy_price} sell={s.sell_price} pnl_7d={s.pnl_7d_pct}%")

        forecasts = await client.trading_bot.fast_forecasts()
        for f in forecasts.forecasts:
            print(f"{f.pair}: {f.signal} conf={f.conf}")

        accuracy = await client.trading_bot.forecast_accuracy()
        print(f"1h MAE: {accuracy.horizon_1h.mae_pct}%")

asyncio.run(main())
```

## Authenticated Usage

```python
async with BitbankClient(api_key="your-api-key") as client:
    # Trading signals (subscriber only)
    signals = await client.trading_bot.signals()

    # Equity curve
    equity = await client.trading_bot.equity_curve()
    print(f"Return: {equity.summary.total_return_pct}%")

    # Trade history (paginated)
    trades = await client.trading_bot.trades(limit=50, offset=0)
    while trades.has_next:
        trades = await client.trading_bot.trades(limit=50, offset=trades.offset + trades.limit)

    # Custom time series forecast (costs credits)
    from bitbank.models.forecasts import LineForecastRequest
    result = await client.forecasts.line(
        LineForecastRequest(series=[100.0, 101.0, 99.5, ...], prediction_length=24)
    )
    print(result.forecast.median)
```

## Sync Client

```python
from bitbank import BitbankSyncClient

client = BitbankSyncClient()
signals = client.trading_bot.public_signals_latest()
client.close()
```

## WebSocket

```python
async with BitbankClient(api_key="your-key") as client:
    ws = client.websocket()
    ws.on("features_update", lambda msg: print(msg))
    ws.on("live_prices", lambda msg: print(msg))

    await ws.connect()
    await ws.subscribe("BTC_USDT")
    await ws.subscribe_live(["BTC_USDT", "ETH_USDT"])

    # ... keep running ...
    await ws.disconnect()
```

## Endpoint Groups

| Group | Description |
|-------|-------------|
| `client.trading_bot` | Signals, equity curve, trades, PnL, performance |
| `client.forecasts` | Coin forecasts, hourly/daily, custom line forecasts |
| `client.auth` | Login, signup, session management |
| `client.account` | API usage, credits, auto top-up settings |

## Error Handling

```python
from bitbank import BitbankClient, AuthenticationError, InsufficientCreditsError

try:
    result = await client.trading_bot.signals()
except AuthenticationError:
    print("Invalid API key")
except InsufficientCreditsError:
    print("Need more credits")
```

## Related

- [bitbank-sdk-typescript](https://github.com/lee101/bitbank-sdk-typescript) - TypeScript SDK
- [bitbank-sdk-go](https://github.com/lee101/bitbank-sdk-go) - Go SDK
- [bitbank-binance-bot](https://github.com/lee101/bitbank-binance-bot) - Trading bot using this SDK

## License

MIT
