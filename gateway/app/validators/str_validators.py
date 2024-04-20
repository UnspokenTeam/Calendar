def str_length_validator(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value is not a string")

    if len(value) == 0:
        raise ValueError("Empty value")

    return value


def str_special_characters_validator(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Value is not a string")

    if "\"" in value or "\'" in value:
        raise ValueError("Value contains reserved characters")

    return value
