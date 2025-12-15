from dataclasses import dataclass
from typing import Optional

from ..models.parking_lot import ParkingLot
from ..models.vehicle import Vehicle
from ..models.electric_vehicle import ElectricVehicle
from ..strategies.allocation_strategy import AllocationStrategy


@dataclass
class ParkingController:
    lot: ParkingLot
    allocation_strategy: AllocationStrategy

    def create_lot(self, level: int, regular_capacity: int, ev_capacity: int) -> None:
        self.lot.level = level
        self.lot.regular_capacity = regular_capacity
        self.lot.ev_capacity = ev_capacity
        self.lot.__post_init__()

    def park(self, vehicle: Vehicle) -> Optional[int]:
        return self.allocation_strategy.allocate(self.lot, vehicle)  # type: ignore[arg-type]

    def park_ev(self, vehicle: ElectricVehicle) -> Optional[int]:
        return self.allocation_strategy.allocate(self.lot, vehicle)  # type: ignore[arg-type]

    def leave(self, slot_number: int, is_ev: bool) -> bool:
        return self.lot.leave(slot_number, is_ev)
