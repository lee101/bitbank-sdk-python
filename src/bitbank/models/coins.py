from __future__ import annotations

from pydantic import BaseModel

__all__ = ["Coin"]


class Coin(BaseModel):
    model_config = {"extra": "allow"}
    currency_pair: str = ""
    name: str = ""
    symbol: str = ""
    price: float | None = None
    change_24h: float | None = None
    volume_24h: float | None = None
