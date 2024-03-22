"""Singleton decorator"""
from typing import TypeVar, Type

T = TypeVar("T")


def singleton(class_: Type[T]) -> Type[T]:
    """
    Decorator to create classes with singleton pattern

    Parameters
    ----------
    class_ : Type[T]
        Any class

    Returns
    -------
    Type[T]
        The class instance
    """
    _instances: dict[Type[T]] = {}

    def wrapper(*args, **kwargs) -> Type[T]:
        if class_ not in _instances:
            _instances[class_] = class_(*args, **kwargs)

        return _instances[class_]

    return wrapper
