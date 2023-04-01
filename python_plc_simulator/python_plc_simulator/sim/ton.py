from .base_sim import BaseSim

import async_state_machine as sm

from ..models import SignalBool


class States(sm.StatesEnum):
    """Состояния таймера."""

    off = sm.enum_auto()
    off_to_on = sm.enum_auto()
    on = sm.enum_auto()


class Ton(BaseSim):
    """Таймер - задержка включения."""

    def __init__(self, input: SignalBool, delay: float) -> None:
        """Таймер - задержка включения."""
        super().__init__()
        self.__input = input
        self.__sm = sm.StateMachine(
            states=[
                sm.State(
                    name=States.off,
                    on_run=[self.__state__off__on_run],
                ),
                sm.State(
                    name=States.off_to_on,
                    on_run=[self.__state__off_to_on__on_run],
                ).config_timeout_on_run(delay, States.on),
                sm.State(
                    name=States.on,
                    on_run=[self.__state__on__on_run],
                ),
            ],
            init_state=States.off,
            states_enum=States,
        )

    @property
    def output(self) -> bool:
        return self.__sm.active_state.name == States.on

    async def run(self):
        await self.__sm.run()

    async def __state__off__on_run(self):
        if self.__input.value:
            raise sm.NewStateException(States.off_to_on)

    async def __state__off_to_on__on_run(self):
        if not self.__input.value:
            raise sm.NewStateException(States.off)

    async def __state__on__on_run(self):
        if not self.__input.value:
            raise sm.NewStateException(States.off)
