from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bitbank.models.account import ApiUsage, AutotopupSettings, CreditsPurchase, UsageEntry

if TYPE_CHECKING:
    from bitbank._http import HttpTransport


class AccountEndpoints:
    def __init__(self, http: HttpTransport):
        self._http = http

    async def api_usage(self) -> ApiUsage:
        data = await self._http.post("/api/get-api-usage")
        return ApiUsage.model_validate(data)

    async def usage_history(self, user_id: str) -> list[UsageEntry]:
        data = await self._http.get(f"/api/usage-history/{user_id}")
        items = data if isinstance(data, list) else data.get("results", [])
        return [UsageEntry.model_validate(e) for e in items]

    async def regenerate_key(self) -> dict[str, Any]:
        return await self._http.post("/api/regenerate-key")

    async def purchase_credits(self, amount_usd: float) -> CreditsPurchase:
        data = await self._http.post("/api/purchase-credits", json={"amount": amount_usd})
        return CreditsPurchase.model_validate(data)

    async def save_autotopup(self, enabled: bool, threshold: float, amount: float) -> dict[str, Any]:
        return await self._http.post(
            "/api/save-autotopup-settings",
            json={"autotopup_enabled": enabled, "autotopup_threshold": threshold, "autotopup_amount": amount},
        )

    async def get_autotopup(self) -> AutotopupSettings:
        data = await self._http.post("/api/autotopup-settings")
        return AutotopupSettings.model_validate(data)
