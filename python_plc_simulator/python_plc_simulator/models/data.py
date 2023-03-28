from dataclasses import asdict, dataclass

from .register import RegisterBase

from .device import DeviceBase


@dataclass
class DataBase:
    @property
    def all_registres(self) -> tuple[RegisterBase, ...]:
        devices: list[DeviceBase] = asdict(self).values()  # type: ignore
        registers = (dev.registers for dev in devices)
        return tuple(*registers)
