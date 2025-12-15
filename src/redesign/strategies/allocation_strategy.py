from abc import ABC, abstractmethod
from typing import Optional
from ..models.parking_lot import ParkingLot
from ..models.vehicle import Vehicle
from ..models.electric_vehicle import ElectricVehicle


class AllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, lot: ParkingLot, vehicle: Vehicle) -> Optional[int]:
        raise NotImplementedError


class RegularFirstStrategy(AllocationStrategy):
    def allocate(self, lot: ParkingLot, vehicle: Vehicle) -> Optional[int]:
        return lot.park_regular(vehicle)


class ElectricOnlyStrategy(AllocationStrategy):
    def allocate(self, lot: ParkingLot, vehicle: ElectricVehicle) -> Optional[int]:
        return lot.park_ev(vehicle)
