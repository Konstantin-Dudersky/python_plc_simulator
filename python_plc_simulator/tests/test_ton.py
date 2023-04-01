import asyncio

from python_plc_simulator.sim import Ton
from python_plc_simulator.models import SignalBool
from python_plc_simulator.models.register import RegisterOutput
from python_plc_simulator.runner import Runner


class StopTestError(Exception):
    pass


def test_on():
    sig = SignalBool(RegisterOutput(), 0)
    ton = Ton(input=sig, delay=0.1)

    async def func():
        assert ton.output == False
        sig.value = True
        assert ton.output == False
        await asyncio.sleep(0.2)
        assert ton.output == True
        raise StopTestError

    runner = Runner((func(), ton.run()), catch_exception=False)
    try:
        asyncio.run(runner())
    except* StopTestError:
        pass


def test_reset_before_delay():
    sig = SignalBool(RegisterOutput(), 0)
    ton = Ton(input=sig, delay=5)

    async def func():
        assert ton.output == False
        sig.value = True
        assert ton.output == False
        await asyncio.sleep(0.2)
        assert ton.output == False
        sig.value = False
        assert ton.output == False
        await asyncio.sleep(0.2)
        assert ton.output == False
        raise StopTestError

    runner = Runner((func(), ton.run()), catch_exception=False)
    try:
        asyncio.run(runner())
    except* StopTestError:
        pass


def test_on_off_on():
    sig = SignalBool(RegisterOutput(), 0)
    ton = Ton(input=sig, delay=0.1)

    async def func():
        sig.value = True
        assert ton.output == False
        await asyncio.sleep(0.2)
        assert ton.output == True

        sig.value = False
        await asyncio.sleep(0.05)
        print("after 0")
        assert ton.output == False

        sig.value = True
        assert ton.output == False
        await asyncio.sleep(0.2)
        assert ton.output == True
        raise StopTestError

    runner = Runner(
        (
            func(),
            ton.run(),
        ),
        catch_exception=False,
    )
    try:
        asyncio.run(runner(), debug=True)
    except* StopTestError:
        pass
