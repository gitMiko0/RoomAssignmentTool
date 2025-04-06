"""
Module Name: room.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Contains the Room class used to represent a physical space 
and manage its booking schedule based on group assignment.

Module Summary:
This module defines the Room data structure which includes:
- Read-only access to its core attributes
- Schedule management functions (add, remove, clear)
- Conversion from raw dictionary (CSV row)

Key Functions:
- `add_booking`, `remove_last_booking`, `clear_schedule`
- Static method `from_dict`

Dependencies:
- `Group` class from group.py
- `datetime` for schedule representation

Known/Suspected Errors:
- None known at this time.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple
from .group import Group

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
        """
        __post_init__
            Validates that room capacity is greater than 0.

        Raises:
            ValueError - if the room capacity is not positive
        """
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
    def schedule(self):
        """
        schedule
            Returns a defensive copy of the schedule list.

        Return Value:
            List[Tuple[datetime, datetime, Group]] - the list of current room bookings
        """
        return self._schedule.copy()

    def add_booking(self, start: datetime, end: datetime, group: Group):
        """
        add_booking
            Adds a new booking for a group into the room's schedule.

        Parameters:
            start (datetime) - start time of the booking
            end (datetime) - end time of the booking
            group (Group) - the group being assigned
        """
        self._schedule.append((start, end, group))

    def remove_last_booking(self):
        """
        remove_last_booking
            Removes the most recent booking added to the room’s schedule.
        """
        if self._schedule:
            self._schedule.pop()

    def clear_schedule(self):
        """
        clear_schedule
            Empties the entire room schedule.
        """
        self._schedule.clear()

    @staticmethod
    def from_dict(data: dict) -> 'Room':
        """
        from_dict
            Converts a dictionary representation of a room (e.g., from CSV) into a Room object.

        Parameters:
            data (dict) - raw room data with fields: RoomID, Capacity, WheelchairAccess, Projector, Computer, FloorLevel

        Return Value:
            Room - the constructed Room object
        """
        return Room(
            _room_id=data['RoomID'],
            _capacity=int(data['Capacity']),
            _wheelchair_access=data['WheelchairAccess'].upper() == 'TRUE',
            _projector=data['Projector'].upper() == 'TRUE',
            _computer=data['Computer'].upper() == 'TRUE',
            _floor_level=int(data['FloorLevel'])
        )
