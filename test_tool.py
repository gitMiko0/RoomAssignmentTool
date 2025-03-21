import pytest
from datetime import datetime, timedelta
from solver import (
    assign_groups, is_valid_assignment, check_floor_preference, check_room_capacity,
    check_wheelchair_access, check_equipment, check_time_overlap, preprocess_data
)

# Functions to easily create sample test data
def sample_group(start, end, size=5, wheelchair=False, projector=False, computer=False, floor=-1, date="2023-01-01"):
    return {
        "GroupID": "G1",
        "Start": datetime.strptime(f"{date} {start}", "%Y-%m-%d %H:%M"),
        "End": datetime.strptime(f"{date} {end}", "%Y-%m-%d %H:%M"),
        "Size": str(size),
        "WheelchairAccess": "TRUE" if wheelchair else "FALSE",
        "Projector": "TRUE" if projector else "FALSE",
        "Computer": "TRUE" if computer else "FALSE",
        "FloorPreference": str(floor)
    }

def sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1):
    return {
        "RoomID": room_id,
        "Capacity": str(capacity),
        "WheelchairAccess": "TRUE" if wheelchair else "FALSE",
        "Projector": "TRUE" if projector else "FALSE",
        "Computer": "TRUE" if computer else "FALSE",
        "FloorLevel": str(floor),
        "Schedule": []  # Added Schedule field
    }

# Unit tests for constraint functions
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
    global TIME_GAP
    TIME_GAP = 10  # Ensure global variable is set

    # Create room with existing booking
    room = sample_room()
    room['Schedule'] = [(datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 11, 0), None)]

    # Valid cases
    assert check_time_overlap(sample_group("11:10", "12:00"), room) is True
    assert check_time_overlap(sample_group("08:10", "09:50"), room) is True
    
    # Invalid cases
    assert check_time_overlap(sample_group("10:30", "11:30"), room) is False
    assert check_time_overlap(sample_group("11:00", "12:00"), room) is False
    assert check_time_overlap(sample_group("10:15", "10:45"), room) is False
    assert check_time_overlap(sample_group("09:50", "11:10"), room) is False

def test_is_valid_assignment():
    # Test valid assignment
    room = sample_room()
    room['Schedule'] = []
    assert is_valid_assignment(sample_group("10:00", "11:00"), room) is True
    
    # Test capacity constraint
    assert is_valid_assignment(sample_group("10:00", "11:00", size=15), sample_room(capacity=10)) is False

def test_backtrack_simple_case():
    groups = [sample_group("10:00", "11:00")]
    rooms = [sample_room()]
    processed_groups, sorted_rooms = preprocess_data(groups, rooms)
    result = assign_groups(processed_groups, sorted_rooms)
    assert len(result) == 1
    assert result[0]["RoomID"] == "R1"

def test_backtrack_conflict():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=False, projector=False, computer=False, floor=1),
        sample_group("11:00", "12:20", size=5, wheelchair=False, projector=False, computer=False, floor=1)
    ]
    rooms = [sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1)]
    
    processed_groups, sorted_rooms = preprocess_data(groups, rooms)
    result = assign_groups(processed_groups, sorted_rooms)
    
    assert len(result) == 0 # none are assigned due to overlap, there is no valid solution for this input.

def test_backtrack_multiple_rooms():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=True, projector=True, computer=True, floor=1),
        sample_group("10:30", "11:30", size=5, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    rooms = [
        sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1),
        sample_room(room_id="R2", capacity=10, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    
    processed_groups, sorted_rooms = preprocess_data(groups, rooms)
    result = assign_groups(processed_groups, sorted_rooms)
    
    assert len(result) == 2  # Both groups should be assigned (but in different rooms due to time overlap)
    assigned_rooms = {r["RoomID"] for r in result}
    assert "R1" in assigned_rooms and "R2" in assigned_rooms  # Ensure different rooms are used

if __name__ == "__main__":
    pytest.main()
