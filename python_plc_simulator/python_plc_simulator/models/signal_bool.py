from typing import Callable

from .register import RegisterBase


def set_bit(value: int, bit: int) -> int:
    return value | (1 << bit)


def reset_bit(value: int, bit: int) -> int:
    return value & ~(1 << bit)


class SignalBool:
    def __init__(self, register: RegisterBase, number: int) -> None:
        self.__register = register
        self.__number = number

    @property
    def value(self) -> bool:
        return False

    @value.setter
    def value(self, value: bool) -> None:
        func: Callable[[int, int], int] = set_bit if value else reset_bit
        self.__register.value = func(self.__register.value, self.__number)
