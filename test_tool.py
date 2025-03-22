import pytest
from datetime import datetime, timedelta
from solver import (
    assign_groups, is_valid_assignment, check_floor_preference, check_room_capacity,
    check_wheelchair_access, check_equipment, check_time_overlap, preprocess_data
)

# Directly create properly typed test data
def sample_group(start, end, size=5, wheelchair=False, projector=False, computer=False, 
                floor=-1, date_str="2023-01-01", group_id="G1"):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return {
        "GroupID": group_id,
        "Start": datetime.combine(date, datetime.strptime(start, "%H:%M").time()),
        "End": datetime.combine(date, datetime.strptime(end, "%H:%M").time()),
        "Size": size,
        "WheelchairAccess": wheelchair,
        "Projector": projector,
        "Computer": computer,
        "FloorPreference": floor
    }

def sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1):
    return {
        "RoomID": room_id,
        "Capacity": capacity,
        "WheelchairAccess": wheelchair,
        "Projector": projector,
        "Computer": computer,
        "FloorLevel": floor,
        "Schedule": []
    }

# Unit tests with proper type handling
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
    
    # Add existing booking (10:00-11:00)
    existing_group = sample_group("10:00", "11:00")
    room['Schedule'] = [(existing_group['Start'], existing_group['End'], existing_group)]

    # Valid cases (no overlap with buffer)
    assert check_time_overlap(sample_group("11:10", "12:00"), room) is True  # Exactly at buffer boundary
    assert check_time_overlap(sample_group("08:10", "09:50"), room) is True   # Before buffer zone
    
    # Invalid cases (overlaps with buffer)
    assert check_time_overlap(sample_group("10:30", "11:30"), room) is False  # Direct overlap
    assert check_time_overlap(sample_group("11:00", "12:00"), room) is False  # Adjacent with buffer
    assert check_time_overlap(sample_group("10:15", "10:45"), room) is False  # Inside original time
    assert check_time_overlap(sample_group("09:50", "11:10"), room) is False  # Wraps buffered time


def test_is_valid_assignment():
    room = sample_room()
    assert is_valid_assignment(sample_group("10:00", "11:00"), room) is True
    assert is_valid_assignment(sample_group("10:00", "11:00", size=15), sample_room(capacity=10)) is False

def test_backtrack_simple_case():
    groups = [sample_group("10:00", "11:00")]
    rooms = [sample_room()]
    result = assign_groups(groups, rooms)
    assert len(result) == 1
    assert result[0]["RoomID"] == "R1"

def test_backtrack_conflict():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=False, projector=False, computer=False, floor=1),
        sample_group("11:00", "12:20", size=5, wheelchair=False, projector=False, computer=False, floor=1)
    ]
    rooms = [sample_room(capacity=10, floor=1)]
    result = assign_groups(groups, rooms)
    assert len(result) == 0

def test_backtrack_multiple_rooms():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=True, projector=True, computer=True, floor=1),
        sample_group("10:30", "11:30", size=5, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    rooms = [
        sample_room(room_id="R1", floor=1),
        sample_room(room_id="R2", floor=1)
    ]
    result = assign_groups(groups, rooms)
    assert len(result) == 2
    assert {r["RoomID"] for r in result} == {"R1", "R2"}

if __name__ == "__main__":
    pytest.main()
