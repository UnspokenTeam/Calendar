# mypy: ignore-errors
"""Singleton decorator"""


def singleton(cls):
    """
    Decorator to create classes with singleton pattern

    Parameters
    ----------
    cls
        Any class

    Returns
    -------
    The class instance

    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return wrapper
