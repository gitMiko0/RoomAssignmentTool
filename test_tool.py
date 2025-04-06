import pytest
from datetime import datetime
from src.solver import assign_groups, is_valid_assignment
from src.constraints import (
    check_floor_preference, check_room_capacity, check_wheelchair_access,
    check_equipment, check_time_overlap
)
from src.room import Room
from src.group import Group

def sample_group(
    start: str,
    end: str,
    size: int = 5,
    wheelchair: bool = False,
    projector: bool = False,
    computer: bool = False,
    floor: int = -1,
    date_str: str = "2023-01-01",
    group_id: str = "G1"
) -> Group:
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
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

def sample_room(
    room_id: str = "R1",
    capacity: int = 10,
    wheelchair: bool = True,
    projector: bool = True,
    computer: bool = True,
    floor: int = 1
) -> Room:
    return Room(
        _room_id=room_id,
        _capacity=capacity,
        _wheelchair_access=wheelchair,
        _projector=projector,
        _computer=computer,
        _floor_level=floor
    )

# === Unit Tests ===
def test_check_floor_preference():
    assert check_floor_preference(sample_group("10:00", "11:00", floor=-1), sample_room(floor=2)) is True
    assert check_floor_preference(sample_group("10:00", "11:00", floor=2), sample_room(floor=2)) is True
    assert check_floor_preference(sample_group("10:00", "11:00", floor=3), sample_room(floor=2)) is False

def test_check_room_capacity():
    assert check_room_capacity(sample_group("10:00", "11:00", size=10), sample_room(capacity=10)) is True
    assert check_room_capacity(sample_group("10:00", "11:00", size=11), sample_room(capacity=10)) is False
    assert check_room_capacity(sample_group("10:00", "11:00", size=9), sample_room(capacity=10)) is True

def test_check_wheelchair_access():
    assert check_wheelchair_access(sample_group("10:00", "11:00", wheelchair=True), sample_room(wheelchair=True)) is True
    assert check_wheelchair_access(sample_group("10:00", "11:00", wheelchair=True), sample_room(wheelchair=False)) is False

def test_check_equipment():
    assert check_equipment(sample_group("10:00", "11:00", projector=True, computer=True), sample_room(projector=True, computer=True)) is True
    assert check_equipment(sample_group("10:00", "11:00", projector=True, computer=False), sample_room(projector=False, computer=True)) is False

def test_check_time_overlap():
    room = sample_room()
    existing_group = sample_group("10:00", "11:00")
    room.add_booking(existing_group.start, existing_group.end, existing_group)

    assert check_time_overlap(sample_group("11:10", "12:00"), room, time_gap=10) is True
    assert check_time_overlap(sample_group("08:10", "09:50"), room, time_gap=10) is True
    assert check_time_overlap(sample_group("10:30", "11:30"), room, time_gap=10) is False
    assert check_time_overlap(sample_group("11:00", "12:00"), room, time_gap=10) is False
    assert check_time_overlap(sample_group("10:15", "10:45"), room, time_gap=10) is False
    assert check_time_overlap(sample_group("09:50", "11:10"), room, time_gap=10) is False

def test_is_valid_assignment():
    room = sample_room()
    assert is_valid_assignment(sample_group("10:00", "11:00"), room, time_gap=10) is True
    assert is_valid_assignment(sample_group("10:00", "11:00", size=15), sample_room(capacity=10), time_gap=10) is False

def test_backtrack_simple_case():
    groups = [sample_group("10:00", "11:00")]
    rooms = [sample_room()]
    result = assign_groups(groups, rooms, time_gap=10)
    assigned = [(r.id, r.schedule) for r in result if r.schedule]
    assert len(assigned) == 1
    assert assigned[0][0] == "R1"

def test_backtrack_conflict():
    groups = [
        sample_group("10:00", "11:00", size=5, floor=1),
        sample_group("11:05", "12:20", size=5, floor=1)
    ]
    rooms = [sample_room(capacity=10, floor=1)]
    result = assign_groups(groups, rooms, time_gap=10)

    # Since the second group is too close, backtracking fails entirely, the solver only returns a solution or nothing (error case in main)
    assert result is None



def test_backtrack_multiple_rooms():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=True, projector=True, computer=True, floor=1),
        sample_group("10:30", "11:30", size=5, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    rooms = [
        sample_room(room_id="R1", floor=1),
        sample_room(room_id="R2", floor=1)
    ]
    result = assign_groups(groups, rooms, time_gap=10)
    total_assigned = sum(len(r.schedule) for r in result)
    assert total_assigned == 2
    assert {r.id for r in result if r.schedule} == {"R1", "R2"}

# Optional CLI run
if __name__ == "__main__":
    pytest.main()
