"""Errors"""
from .permission_denied import PermissionDeniedError
from .rate_limit_error import RateLimitError

__all__ = ["PermissionDeniedError", "RateLimitError"]
