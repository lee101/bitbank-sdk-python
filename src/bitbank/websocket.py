from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable

import websockets
from websockets.asyncio.client import ClientConnection

log = logging.getLogger(__name__)

EventCallback = Callable[[dict[str, Any]], None]


class BitbankWebSocket:
    def __init__(self, base_url: str = "wss://bitbank.nz/ws", api_key: str | None = None):
        self.url = base_url
        self.api_key = api_key
        self._ws: ClientConnection | None = None
        self._callbacks: dict[str, list[EventCallback]] = {}
        self._task: asyncio.Task | None = None
        self._reconnect = True
        self._max_retries = 5

    def on(self, event: str, callback: EventCallback) -> None:
        self._callbacks.setdefault(event, []).append(callback)

    async def connect(self) -> None:
        self._reconnect = True
        self._task = asyncio.create_task(self._run())

    async def disconnect(self) -> None:
        self._reconnect = False
        if self._ws:
            await self._ws.close()
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def subscribe(self, pair: str) -> None:
        await self._send({"event": "subscribe", "currency_pair": pair})

    async def unsubscribe(self, pair: str) -> None:
        await self._send({"event": "unsubscribe", "currency_pair": pair})

    async def subscribe_all(self) -> None:
        await self._send({"event": "subscribe_all_pairs"})

    async def subscribe_live(self, pairs: list[str] | None = None) -> None:
        msg: dict[str, Any] = {"event": "subscribe_live"}
        if self.api_key:
            msg["secret"] = self.api_key
        if pairs:
            msg["currency_pairs"] = pairs
        await self._send(msg)

    async def ping(self) -> None:
        await self._send({"event": "ping"})

    async def _send(self, data: dict[str, Any]) -> None:
        if self._ws:
            await self._ws.send(json.dumps(data))

    async def _run(self) -> None:
        retries = 0
        while self._reconnect:
            try:
                async with websockets.connect(self.url) as ws:
                    self._ws = ws
                    retries = 0
                    log.info("ws connected")
                    async for raw in ws:
                        try:
                            msg = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        event = msg.get("event", "")
                        for cb in self._callbacks.get(event, []):
                            cb(msg)
                        for cb in self._callbacks.get("*", []):
                            cb(msg)
            except (websockets.ConnectionClosed, OSError) as e:
                log.warning("ws disconnected: %s", e)
            except Exception as e:
                log.error("ws error: %s", e)

            if not self._reconnect:
                break
            retries += 1
            if retries > self._max_retries:
                log.error("ws max retries exceeded")
                break
            delay = min(2**retries, 30)
            log.info("ws reconnecting in %ds", delay)
            await asyncio.sleep(delay)
        self._ws = None
