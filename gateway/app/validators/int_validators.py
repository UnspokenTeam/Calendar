"""Int validators"""


def int_not_equal_zero_validator(value: int) -> int:
    """
    Checks that given integer is not equal to zero.

    Parameters
    ----------
    value : int
        Integer to be checked.

    Returns
    -------
    int
        Checked integer.

    Raises
    ------
    ValueError
        If given integer is not equal to zero or is not instance of int.

    """
    if not isinstance(value, int):
        raise ValueError('Value must be an integer')

    if value == 0:
        raise ValueError('Value cannot be zero')

    return value
