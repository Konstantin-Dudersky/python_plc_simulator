import asyncio
from dataclasses import dataclass
from ipaddress import IPv4Address

from .logger import Logger
from .modbus_client import ModbusClient
from .models.data import DataBase
from .models.device import SiemensCPU1212

Logger(output_to_console=True)


@dataclass
class Data(DataBase):
    cpu: SiemensCPU1212 = SiemensCPU1212()


data1 = Data()


def main():
    asyncio.run(
        ModbusClient(
            registres=data1.all_registres,
            host=IPv4Address("192.168.101.101"),
        ).cycle(),
    )
    print("dq", data1.cpu.dq_a_0.value)
