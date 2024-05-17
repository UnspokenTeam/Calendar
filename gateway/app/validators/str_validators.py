"""String validators."""
from typing import Optional


def str_special_characters_validator(value: str) -> str:
    """
    Check if string contains special characters.

    Parameters
    ----------
    value : str
        String to be checked.

    Returns
    -------
    str
        String without special characters.

    Raises
    ------
    ValueError
        Raised if string contains special characters or if value is not instance of string.

    """
    if not isinstance(value, str):
        raise ValueError("Value is not a string")

    if '"' in value or "'" in value:
        raise ValueError("Value contains reserved characters")

    return value


def optional_str_special_characters_validator(value: Optional[str]) -> Optional[str]:
    """
    Check if string contains special characters.

    Parameters
    ----------
    value : Optional[str]
        String to be checked.

    Returns
    -------
    Optional[str]
        String without special characters.

    """
    if value is None:
        return value

    return str_special_characters_validator(value)
