import abc

from .register import RegisterBase, RegisterInput, RegisterOutput
from .signal_bool import SignalBool


class DeviceBase(abc.ABC):
    pass


class SiemensCPU1212:
    def __init__(self) -> None:
        self.__reg_di_a = RegisterInput()

        self.__di_a_0 = SignalBool(self.__reg_di_a, 0)
        self.__di_a_1 = SignalBool(self.__reg_di_a, 1)

    @property
    def registers(self) -> tuple[RegisterBase]:
        return (self.__reg_di_a,)

    @property
    def di_a_0(self) -> SignalBool:
        return self.__di_a_0

    @property
    def di_a_1(self) -> SignalBool:
        return self.__di_a_1
