import asyncio

from python_plc_simulator.modbus_client import ModbusClient
from python_plc_simulator.runner import Runner

from .const import IP_ADDRESS
from .device_configuration import device_configuration
from .sim import sim, used_sim_devices


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
    runner.add_task(client.run())  # pyright: ignore
    runner.add_task(sim())
    for sim_device in used_sim_devices:
        runner.add_task(sim_device.run())
    asyncio.run(runner())
