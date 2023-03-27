import asyncio
from dataclasses import dataclass
from ipaddress import IPv4Address

from .modbus_client import ModbusClient

from .data.device import SiemensCPU1212
from .data.data import DataBase


@dataclass
class Data(DataBase):
    cpu: SiemensCPU1212 = SiemensCPU1212()


data1 = Data()

# for key, value in asdict(data1).items():
#     value = cast(DeviceBase, value)
#     print(value.registers)

print(data1.all_registres)


def main():
    asyncio.run(
        ModbusClient(
            registres=data1.all_registres,
            host=IPv4Address("192.168.101.101"),
        ).test()
    )
