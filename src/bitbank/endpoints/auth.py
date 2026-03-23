from __future__ import annotations

from typing import TYPE_CHECKING

from bitbank.models.auth import LoginResponse, SessionResponse, SignupResponse

if TYPE_CHECKING:
    from bitbank._http import HttpTransport


class AuthEndpoints:
    def __init__(self, http: HttpTransport):
        self._http = http

    async def login(self, email: str, password: str) -> LoginResponse:
        data = await self._http.post("/api/login", json={"email": email, "password": password})
        resp = LoginResponse.model_validate(data)
        if resp.secret:
            self._http.api_key = resp.secret
        return resp

    async def signup(self, email: str, password: str, name: str = "") -> SignupResponse:
        payload = {"email": email, "password": password}
        if name:
            payload["name"] = name
        data = await self._http.post("/api/signup", json=payload)
        return SignupResponse.model_validate(data)

    async def session(self) -> SessionResponse:
        data = await self._http.get("/api/session")
        return SessionResponse.model_validate(data)

    async def logout(self) -> None:
        await self._http.post("/api/logout")
        self._http.api_key = None
