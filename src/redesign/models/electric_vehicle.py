from dataclasses import dataclass
from .vehicle import Vehicle


@dataclass
class ElectricVehicle(Vehicle):
    charge_percent: int = 0

    def get_type(self) -> str:
        return "ElectricVehicle"


@dataclass
class ElectricCar(ElectricVehicle):
    def get_type(self) -> str:
        return "ElectricCar"


@dataclass
class ElectricBike(ElectricVehicle):
    def get_type(self) -> str:
        return "ElectricBike"
