from typing import Literal
from ..models.vehicle import Car, Motorcycle, Truck, Vehicle
from ..models.electric_vehicle import ElectricBike, ElectricCar, ElectricVehicle


VehicleKind = Literal["car", "motorcycle", "truck"]


def create_vehicle(kind: VehicleKind, reg: str, make: str, model: str, color: str) -> Vehicle:
    k = kind.lower()
    if k == "car":
        return Car(registration_number=reg, make=make, model=model, color=color)
    if k == "motorcycle":
        return Motorcycle(registration_number=reg, make=make, model=model, color=color)
    if k == "truck":
        return Truck(registration_number=reg, make=make, model=model, color=color)
    raise ValueError(f"Unsupported vehicle kind: {kind}")


def create_electric(kind: Literal["car", "bike"], reg: str, make: str, model: str, color: str) -> ElectricVehicle:
    k = kind.lower()
    if k == "car":
        return ElectricCar(registration_number=reg, make=make, model=model, color=color)
    if k == "bike":
        return ElectricBike(registration_number=reg, make=make, model=model, color=color)
    raise ValueError(f"Unsupported electric vehicle kind: {kind}")
