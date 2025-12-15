from dataclasses import dataclass


@dataclass
class Vehicle:
    registration_number: str
    make: str
    model: str
    color: str

    def get_type(self) -> str:
        return "Vehicle"


@dataclass
class Car(Vehicle):
    def get_type(self) -> str:
        return "Car"


@dataclass
class Truck(Vehicle):
    def get_type(self) -> str:
        return "Truck"


@dataclass
class Motorcycle(Vehicle):
    def get_type(self) -> str:
        return "Motorcycle"
