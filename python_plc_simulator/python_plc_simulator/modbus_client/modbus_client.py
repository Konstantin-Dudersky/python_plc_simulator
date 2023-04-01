import logging
from asyncio import sleep
from ipaddress import IPv4Address
from typing import TypeAlias

import async_state_machine as sm

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse, ModbusResponse

from .exceptions import ConfigError, RequestError
from ..models.register import RegisterBase, RegisterInput, RegisterOutput

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


ResponseType: TypeAlias = ExceptionResponse | ModbusResponse
RegistersType: TypeAlias = RegisterBase | RegisterInput | RegisterOutput


class States(sm.StatesEnum):
    disconnected = sm.enum_auto()
    connected = sm.enum_auto()


class ModbusClient:
    def __init__(
        self,
        registres: tuple[RegistersType, ...],
        host: IPv4Address,
        port: int = 502,
    ) -> None:
        self.__client: AsyncModbusTcpClient
        self.__registers: tuple[RegistersType, ...]
        self.__sm: sm.StateMachine

        self.__client = AsyncModbusTcpClient(
            host=str(host),
            port=port,
            close_comm_on_error=True,
            retries=0,
        )
        self.__registers = registres
        self.__sm = sm.StateMachine(
            states={
                sm.State(
                    name=States.disconnected,
                    on_run=[self.__on_run_disconnected],
                ),
                sm.State(
                    name=States.connected,
                    on_run=[self.__on_run_connected],
                    on_exit=[self.__on_exit_connected],
                ),
            },
            states_enum=States,
            init_state=States.disconnected,
        )

    async def run(self):
        await self.__sm.run()

    async def __on_run_disconnected(self):
        await self.__client.connect()
        if self.__client.connected:
            raise sm.NewStateException(States.connected)
        else:
            await sleep(2)

    async def __on_run_connected(self):
        try:
            await self.__process_registers()
        except RequestError:
            raise sm.NewStateException(States.disconnected)

    async def __on_exit_connected(self):
        await self.__client.close()

    async def __process_registers(self) -> None:
        for address, register in enumerate(self.__registers):
            match register:
                case RegisterInput():
                    await self.__register_write(
                        address=address,
                        value=register.value,
                    )
                case RegisterOutput():
                    register.value = await self.__register_read(
                        address=address,
                    )
                case _:
                    msg = "Неизвестный тип данных регистра: {0}"
                    raise ConfigError(msg.format(type(register)))

    async def __register_write(self, address: int, value: int) -> None:
        try:
            await self.__client.write_register(  # pyright: ignore
                address=address,
                value=value,
            )
        except ModbusException as exc:
            log.error(exc)
            raise RequestError from exc
        except TimeoutError as exc:
            log.error(exc)
            raise RequestError from exc

    async def __register_read(self, address: int) -> int:
        try:
            reg: ResponseType = (
                await self.__client.read_holding_registers(  # pyright: ignore
                    address=address,
                    count=1,
                )
            )
        except ModbusException as exc:
            log.error(exc)
            raise RequestError from exc
        except TimeoutError as exc:
            log.error(exc)
            raise RequestError from exc
        _check_modbus_response(reg)
        return reg.registers[0]  # pyright: ignore


def _check_modbus_response(response: ResponseType) -> ModbusResponse:
    """Check modbus call worked generically."""
    match response:
        case ExceptionResponse():
            raise RequestError
        case ModbusResponse():
            return response
