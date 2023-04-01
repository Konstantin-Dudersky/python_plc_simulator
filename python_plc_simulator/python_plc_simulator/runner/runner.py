"""Класс для запуска асинхронных задач."""

import asyncio
import logging
from typing import Coroutine, Final, Iterable, TypeAlias

TCoro: TypeAlias = Coroutine[None, None, None]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG_BASE_EXCEPTION: Final[
    str
] = "Необработанное исключение, программа заканчивает выполнение"


class Runner(object):
    """Класс для запуска асинхронных задач."""

    def __init__(
        self,
        coros: Iterable[TCoro] | None = None,
        return_when: str = asyncio.FIRST_COMPLETED,
        catch_exception: bool = True,
    ) -> None:
        """Класс для запуска асинхронных задач.

        Parameters
        ----------
        coros: Iterable[TCoro]
            Последовательность корутин. Можно добавлять после инициализации
            через метод add_task
        return_when: str
            Условие остановки выполнения
        """
        self.__coros: set[TCoro] = set(coros) if coros else set()
        self.__return_when = return_when
        self.__catch_exception = catch_exception

    async def __call__(self) -> None:
        try:
            await self.__create_tasks_for_coro()
        except BaseException:  # noqa: WPS424
            log.exception(MSG_BASE_EXCEPTION)
            if not self.__catch_exception:
                raise

    def add_task(self, coro: TCoro) -> None:
        """Добавить задачу для циклического."""
        self.__coros.add(coro)

    async def __create_tasks_for_coro(self) -> None:
        async with asyncio.TaskGroup() as tg:
            for coro in self.__coros:
                tg.create_task(coro)
