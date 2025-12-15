from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from .vehicle import Vehicle
from .electric_vehicle import ElectricVehicle


@dataclass
class ParkingSlot:
    index: int
    is_electric: bool
    vehicle: Optional[Vehicle] = None

    def is_empty(self) -> bool:
        return self.vehicle is None


@dataclass
class ParkingLot:
    level: int
    regular_capacity: int
    ev_capacity: int
    regular_slots: List[ParkingSlot] = field(default_factory=list)
    ev_slots: List[ParkingSlot] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.regular_slots:
            self.regular_slots = [ParkingSlot(i, is_electric=False) for i in range(self.regular_capacity)]
        if not self.ev_slots:
            self.ev_slots = [ParkingSlot(i, is_electric=True) for i in range(self.ev_capacity)]

    def first_empty_regular(self) -> Optional[int]:
        for slot in self.regular_slots:
            if slot.is_empty():
                return slot.index
        return None

    def first_empty_ev(self) -> Optional[int]:
        for slot in self.ev_slots:
            if slot.is_empty():
                return slot.index
        return None

    def park_regular(self, vehicle: Vehicle) -> Optional[int]:
        idx = self.first_empty_regular()
        if idx is None:
            return None
        self.regular_slots[idx].vehicle = vehicle
        return idx + 1

    def park_ev(self, vehicle: ElectricVehicle) -> Optional[int]:
        idx = self.first_empty_ev()
        if idx is None:
            return None
        self.ev_slots[idx].vehicle = vehicle
        return idx + 1

    def leave(self, slot_number: int, is_ev: bool) -> bool:
        slots = self.ev_slots if is_ev else self.regular_slots
        idx = slot_number - 1
        if 0 <= idx < len(slots) and not slots[idx].is_empty():
            slots[idx].vehicle = None
            return True
        return False
