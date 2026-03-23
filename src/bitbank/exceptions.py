from __future__ import annotations


class BitbankError(Exception):
    pass


class BitbankApiError(BitbankError):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        super().__init__(f"[{status_code}] {error_code}: {message}")


class AuthenticationError(BitbankApiError):
    pass


class ForbiddenError(BitbankApiError):
    pass


class NotFoundError(BitbankApiError):
    pass


class InsufficientCreditsError(BitbankApiError):
    pass


class RateLimitError(BitbankApiError):
    pass


class ValidationError(BitbankApiError):
    pass


class ServerError(BitbankApiError):
    pass


class ConnectionError(BitbankError):
    pass


class WebSocketError(BitbankError):
    pass


_STATUS_MAP: dict[int, type[BitbankApiError]] = {
    400: ValidationError,
    401: AuthenticationError,
    402: InsufficientCreditsError,
    403: ForbiddenError,
    404: NotFoundError,
    429: RateLimitError,
}


def map_error(status_code: int, error_code: str, message: str) -> BitbankApiError:
    cls = _STATUS_MAP.get(status_code, ServerError if status_code >= 500 else BitbankApiError)
    return cls(status_code, error_code, message)
