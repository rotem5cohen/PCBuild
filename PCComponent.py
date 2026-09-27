from abc import ABC, abstractmethod
from typing import Set
from typing import Dict


class PCComponent(ABC):

    def __init__(self, brand: str, model: str, price: float, power_draw_w: int):
        self.brand = brand
        self.model = model
        self.price = price
        self.power_draw_w = power_draw_w

    @property
    @abstractmethod
    def component_type(self) -> str:
        pass

    def __str__(self):
        return f"{self.brand} {self.model}"


class CPU(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int, socket: str):
        super().__init__(brand, model, price, power_draw_w)
        self.socket = socket

    @property
    def component_type(self) -> str:
        return "CPU"


class Case(PCComponent):
    def __init__(self, brand: str, model: str, price: float,
                 supported_form_factors: Set[str],
                 max_gpu_length_mm: int,
                 max_radiator_mm: int, max_cpu_cooler_height_mm: int,
                 drive_bays_2_5: int, drive_bays_3_5: int):

        super().__init__(brand, model, price, power_draw_w=0)

        self.supported_form_factors = supported_form_factors
        self.max_gpu_length_mm = max_gpu_length_mm
        self.max_radiator_mm = max_radiator_mm
        self.max_cpu_cooler_height_mm = max_cpu_cooler_height_mm
        self.drive_bays_2_5 = drive_bays_2_5
        self.drive_bays_3_5 = drive_bays_3_5

    @property
    def component_type(self) -> str:
        return "Case"

class MotherBoard(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int,
                 socket: str, form_factor: str, supported_ram_type: str,
                 ram_slots: int, pcie_x16_slots: int,
                  m2_slots: int, sata_ports: int):
        super().__init__(self, brand, model, price, power_draw_w)

        self.socket = socket
        self.form_factor = form_factor
        self.supported_ram_type = supported_ram_type
        self.ram_slots = ram_slots
        self.pcie_x16_slots = pcie_x16_slots
        self.m2_slots = m2_slots
        self.sata_ports = sata_ports

    @property
    def component_type(self) -> str:
        return "Motherboard"


class RAM(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int,
                 ram_type: str, capacity_gb: int, modules: int, speed_mhz: int):
        super().__init__(brand, model, price, power_draw_w)

        self.ram_type = ram_type
        self.capacity_gb = capacity_gb
        self.modules = modules
        self.speed_mhz = speed_mhz

    @property
    def component_type(self) -> str:
        return "RAM"


from typing import Dict


class GPU(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int,
                 length_mm: int, power_connectors: Dict[str, int]):
        super().__init__(brand, model, price, power_draw_w)

        self.length_mm = length_mm
        self.power_connectors = power_connectors

    @property
    def component_type(self) -> str:
        return "GPU"

class PSU(PCComponent):
    def __init__(self, brand: str, model: str, price: float,
                 wattage_w: int, available_connectors: Dict[str, int]):

        super().__init__(brand, model, price, power_draw_w=0)

        self.wattage_w = wattage_w
        self.available_connectors = available_connectors

    @property
    def component_type(self) -> str:
        return "PSU"


from typing import Set, Optional


class Cooler(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int,
                 supported_sockets: Set[str],
                 height_mm: Optional[int] = None,
                 radiator_size_mm: Optional[int] = None):
        super().__init__(brand, model, price, power_draw_w)

        self.supported_sockets = supported_sockets

        self.height_mm = height_mm

        self.radiator_size_mm = radiator_size_mm

        if self.height_mm is None and self.radiator_size_mm is None:
            raise ValueError("Cooler must have either a height (Air) or a radiator size (AIO).")

    @property
    def component_type(self) -> str:
        return "Cooler"


from typing import Dict


class Storage(PCComponent):
    def __init__(self, brand: str, model: str, price: float, power_draw_w: int,
                 capacity_tb: float, form_factor: str, interface: str,
                 power_connectors: Dict[str, int]):
        super().__init__(brand, model, price, power_draw_w)

        self.capacity_tb = capacity_tb
        self.form_factor = form_factor
        self.interface = interface
        self.power_connectors = power_connectors

    @property
    def component_type(self) -> str:
        return "Storage"