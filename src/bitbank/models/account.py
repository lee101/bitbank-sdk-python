from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["ApiUsage", "UsageEntry", "AutotopupSettings", "CreditsPurchase"]


class ApiUsage(BaseModel):
    requests: list[dict] = Field(default_factory=list)
    total: int = 0
    model_config = {"extra": "allow"}


class UsageEntry(BaseModel):
    endpoint: str = ""
    count: int = 0
    total_cost: float = 0.0
    model_config = {"extra": "allow"}


class AutotopupSettings(BaseModel):
    autotopup_enabled: bool = False
    autotopup_threshold: float = 0.0
    autotopup_amount: float = 0.0
    model_config = {"extra": "allow"}


class CreditsPurchase(BaseModel):
    success: bool = False
    credits: float = 0.0
    checkout_url: str = ""
    model_config = {"extra": "allow"}
