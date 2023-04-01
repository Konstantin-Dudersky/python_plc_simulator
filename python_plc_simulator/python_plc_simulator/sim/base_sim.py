import abc


class BaseSim(abc.ABC):
    """Базовый элемент симуляции."""

    def __init__(self) -> None:
        used_sim_devices.add(self)


used_sim_devices: set[BaseSim] = set()
