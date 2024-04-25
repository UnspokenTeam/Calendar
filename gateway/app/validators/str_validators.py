"""String validators."""


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
        Raised if string contains special characters.

    """
    if not isinstance(value, str):
        raise ValueError("Value is not a string")

    if '"' in value or "'" in value:
        raise ValueError("Value contains reserved characters")

    return value