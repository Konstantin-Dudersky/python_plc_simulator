from .register import RegisterBase


class SignalBool:
    def __init__(self, register: RegisterBase, number: int) -> None:
        self.__register = register
        self.__number = number

    @property
    def value(self) -> bool:
        return False

    @value.setter
    def value(self, value: bool) -> None:
        pass
