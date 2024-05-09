"""Errors module."""
from .ai_response_error import AiResponseError
from .invalid_token_error import InvalidTokenError
from .permission_denied_error import PermissionDeniedError
from .unique_error import UniqueError
from .value_not_found_error import ValueNotFoundError
from .wrong_interval_error import WrongIntervalError
from .unauthenticated_error import UnauthenticatedError

__all__ = [
    "UniqueError",
    "AiResponseError",
    "InvalidTokenError",
    "WrongIntervalError",
    "PermissionDeniedError",
    "ValueNotFoundError",
    "UnauthenticatedError"
]
