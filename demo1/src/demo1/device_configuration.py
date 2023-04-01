from dataclasses import dataclass

from python_plc_simulator.models import DeviceConfigurationBase, devices


@dataclass
class DeviceConfiguration(DeviceConfigurationBase):
    cpu: devices.SiemensCPU1212 = devices.SiemensCPU1212()


device_configuration = DeviceConfiguration()
