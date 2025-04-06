from src.room import Room
from src.group import Group
from datetime import datetime

def sample_group(start: str, end: str, size=5, wheelchair=False, projector=False, computer=False, floor=-1, group_id="G1"):
    # for simplification
    date = datetime.strptime("2023-01-01", "%Y-%m-%d").date()
    start_time = datetime.combine(date, datetime.strptime(start, "%H:%M").time())
    end_time = datetime.combine(date, datetime.strptime(end, "%H:%M").time())
    return Group(
        _group_id=group_id,
        _start=start_time,
        _end=end_time,
        _size=size,
        _wheelchair_access=wheelchair,
        _projector=projector,
        _computer=computer,
        _floor_preference=floor
    )

def sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1):
    return Room(
        _room_id=room_id,
        _capacity=capacity,
        _wheelchair_access=wheelchair,
        _projector=projector,
        _computer=computer,
        _floor_level=floor
    )