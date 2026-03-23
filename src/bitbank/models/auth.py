from __future__ import annotations

from pydantic import BaseModel

__all__ = ["UserInfo", "LoginResponse", "SessionResponse", "SignupResponse"]


class UserInfo(BaseModel):
    id: str = ""
    email: str = ""
    name: str = ""
    secret: str = ""
    model_config = {"extra": "allow"}


class LoginResponse(BaseModel):
    success: bool = False
    user: UserInfo | None = None
    secret: str = ""


class SessionResponse(BaseModel):
    user: UserInfo | None = None


class SignupResponse(BaseModel):
    success: bool = False
    user: UserInfo | None = None
    message: str = ""
