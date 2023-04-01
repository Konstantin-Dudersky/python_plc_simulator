import asyncio
from loguru import logger
from python_plc_simulator.sim import used_sim_devices, Ton

from .device_configuration import device_configuration

ton = Ton(input=device_configuration.cpu.dq_a_0, delay=30)

logger.info(used_sim_devices)


async def sim():
    while True:
        device_configuration.cpu.di_a_0.value = ton.output
        await asyncio.sleep(0.1)
