from dataclasses import dataclass
from datetime import datetime

@dataclass
class Group:
    _group_id: str
    _start: datetime
    _end: datetime
    _size: int
    _wheelchair_access: bool
    _projector: bool
    _computer: bool
    _floor_preference: int

    def __post_init__(self):
        if self._start >= self._end:
            raise ValueError("Start time must be before end time.")
        if self._size <= 0:
            raise ValueError("Group size must be positive.")

    # Public getters
    @property
    def id(self): return self._group_id

    @property
    def start(self): return self._start

    @property
    def end(self): return self._end

    @property
    def size(self): return self._size

    @property
    def wheelchair_access(self): return self._wheelchair_access

    @property
    def projector(self): return self._projector

    @property
    def computer(self): return self._computer

    @property
    def floor_preference(self): return self._floor_preference

    @staticmethod
    def from_dict(data: dict) -> 'Group':
        return Group(
            _group_id=data['GroupID'],
            _start=datetime.strptime(data['Start'], "%Y-%m-%d %H:%M"),
            _end=datetime.strptime(data['End'], "%Y-%m-%d %H:%M"),
            _size=int(data['Size']),
            _wheelchair_access=data['WheelchairAccess'].upper() == 'TRUE',
            _projector=data['Projector'].upper() == 'TRUE',
            _computer=data['Computer'].upper() == 'TRUE',
            _floor_preference=int(data['FloorPreference'])
        )
