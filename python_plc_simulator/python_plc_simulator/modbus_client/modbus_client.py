from enum import StrEnum, auto
from ipaddress import IPv4Address
from typing import Any

from pymodbus.client import AsyncModbusTcpClient

from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse, ModbusResponse

from .exceptions import RequestError
from ..data.register import RegisterBase, RegisterInput, RegisterOutput


class States(StrEnum):
    disconnected = auto()
    connected = auto()


class ModbusClient:
    def __init__(
        self,
        registres: tuple[RegisterBase, ...],
        host: IPv4Address,
        port: int = 502,
    ) -> None:
        self.__client: AsyncModbusTcpClient
        self.__state: States

        self.__client = AsyncModbusTcpClient(
            host=str(host),
            port=port,
        )
        self.__state = States.disconnected

    async def test(self):
        await self.__client.connect()
        print(self.__client.connected)
        try:
            rh = await self.__client.read_holding_registers(  # pyright: ignore
                address=0,
                count=4,
            )
        except ModbusException as exc:
            print(exc)
        self._check_call(rh)
        print(rh)

    def _check_call(
        self, rr: ExceptionResponse | ModbusResponse
    ) -> ModbusResponse:
        """Check modbus call worked generically."""
        match rr:
            case ExceptionResponse():
                print(rr)
                raise RequestError
            case ModbusResponse():
                print("!!!!!!!!!")
                return rr
