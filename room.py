from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple
from group import Group

@dataclass
class Room:
    _room_id: str
    _capacity: int
    _wheelchair_access: bool
    _projector: bool
    _computer: bool
    _floor_level: int
    _schedule: List[Tuple[datetime, datetime, Group]] = field(default_factory=list)

    def __post_init__(self):
        if self._capacity <= 0:
            raise ValueError("Room capacity must be positive.")

    # Public getters -- This data structure is read-only
    @property
    def id(self): return self._room_id

    @property
    def capacity(self): return self._capacity

    @property
    def wheelchair_access(self): return self._wheelchair_access

    @property
    def projector(self): return self._projector

    @property
    def computer(self): return self._computer

    @property
    def floor_level(self): return self._floor_level

    @property
    def schedule(self): return self._schedule.copy()  # Return a safe copy

    def add_booking(self, start: datetime, end: datetime, group: Group):
        self._schedule.append((start, end, group))

    def remove_last_booking(self):
        if self._schedule:
            self._schedule.pop()

    def clear_schedule(self):
        self._schedule.clear()

    # for raw CSV data
    @staticmethod
    def from_dict(data: dict) -> 'Room':
        return Room(
            _room_id=data['RoomID'],
            _capacity=int(data['Capacity']),
            _wheelchair_access=data['WheelchairAccess'].upper() == 'TRUE',
            _projector=data['Projector'].upper() == 'TRUE',
            _computer=data['Computer'].upper() == 'TRUE',
            _floor_level=int(data['FloorLevel'])
        )
