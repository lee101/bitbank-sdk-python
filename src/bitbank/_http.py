from __future__ import annotations

from typing import Any

import httpx

from bitbank.exceptions import ConnectionError, map_error


class HttpTransport:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=timeout)

    def _headers(self) -> dict[str, str]:
        h: dict[str, str] = {}
        if self.api_key:
            h["X-API-Key"] = self.api_key
        return h

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return await self._request("POST", path, json=json)

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.base_url}{path}"
        try:
            resp = await self._client.request(method, url, headers=self._headers(), **kwargs)
        except httpx.HTTPError as e:
            raise ConnectionError(str(e)) from e

        if resp.status_code >= 400:
            try:
                body = resp.json()
            except Exception:
                body = {"error": "unknown", "message": resp.text}
            error_code = body.get("error", "")
            message = body.get("message", body.get("detail", str(body)))
            raise map_error(resp.status_code, error_code, message)

        if resp.status_code == 204:
            return {}
        return resp.json()

    async def close(self) -> None:
        await self._client.aclose()
