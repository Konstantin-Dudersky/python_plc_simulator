import asyncio

from python_plc_simulator.modbus_client import ModbusClient
from python_plc_simulator.runner import Runner

from .device_configuration import device_configuration
from .const import IP_ADDRESS

from python_plc_simulator.logger import Logger


async def print_():
    while True:
        # print("dq", device_configuration.cpu.dq_a_0.value)
        await asyncio.sleep(1)
        # raise ValueError


def main():
    runner = Runner()
    client = ModbusClient(
        registres=device_configuration.all_registres,
        host=IP_ADDRESS,
    )
    runner.add_task(client.run())
    runner.add_task(print_())
    asyncio.run(runner())
