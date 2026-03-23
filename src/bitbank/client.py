from __future__ import annotations

import asyncio
from typing import Any

from bitbank._http import HttpTransport
from bitbank.endpoints.account import AccountEndpoints
from bitbank.endpoints.auth import AuthEndpoints
from bitbank.endpoints.forecasts import ForecastEndpoints
from bitbank.endpoints.trading_bot import TradingBotEndpoints
from bitbank.websocket import BitbankWebSocket

DEFAULT_BASE_URL = "https://bitbank.nz"


class BitbankClient:
    """Async client for the bitbank.nz API."""

    def __init__(self, api_key: str | None = None, base_url: str = DEFAULT_BASE_URL, timeout: float = 30.0):
        self._http = HttpTransport(base_url, api_key=api_key, timeout=timeout)
        self.trading_bot = TradingBotEndpoints(self._http)
        self.forecasts = ForecastEndpoints(self._http)
        self.auth = AuthEndpoints(self._http)
        self.account = AccountEndpoints(self._http)

    def websocket(self, url: str | None = None) -> BitbankWebSocket:
        ws_url = url or self._http.base_url.replace("http", "ws") + "/ws"
        return BitbankWebSocket(ws_url, api_key=self._http.api_key)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> BitbankClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class BitbankSyncClient:
    """Sync wrapper around BitbankClient."""

    def __init__(self, api_key: str | None = None, base_url: str = DEFAULT_BASE_URL, timeout: float = 30.0):
        self._async = BitbankClient(api_key=api_key, base_url=base_url, timeout=timeout)
        self._loop: asyncio.AbstractEventLoop | None = None

    def _run(self, coro: Any) -> Any:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(asyncio.run, coro).result()
        return asyncio.run(coro)

    @property
    def trading_bot(self) -> _SyncProxy:
        return _SyncProxy(self._async.trading_bot, self._run)

    @property
    def forecasts(self) -> _SyncProxy:
        return _SyncProxy(self._async.forecasts, self._run)

    @property
    def auth(self) -> _SyncProxy:
        return _SyncProxy(self._async.auth, self._run)

    @property
    def account(self) -> _SyncProxy:
        return _SyncProxy(self._async.account, self._run)

    def close(self) -> None:
        self._run(self._async.close())


class _SyncProxy:
    def __init__(self, target: Any, runner: Any):
        self._target = target
        self._runner = runner

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return self._runner(attr(*args, **kwargs))
            return wrapper
        return attr
