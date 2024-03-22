from typing import TypeVar, Type

T = TypeVar("T")


def singleton(class_: Type[T]) -> Type[T]:
    """
    Decorator to create singleton classes

    :param class_: Any class
    :return: The class instance
    """
    _instances: dict[Type[T]] = {}

    def wrapper(*args, **kwargs) -> Type[T]:
        if class_ not in _instances:
            _instances[class_] = class_(*args, **kwargs)

        return _instances[class_]

    return wrapper
