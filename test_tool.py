import pytest
from datetime import datetime, timedelta
from solver import (
    backtrack, is_valid_assignment, check_floor_preference, check_room_capacity,
    check_wheelchair_access, check_equipment, check_time_overlap
)

# Sample test data
def sample_group(start, end, size=5, wheelchair=False, projector=False, computer=False, floor=-1, date="2023-01-01"):
    return {
        "GroupID": "G1",
        "Start": f"{date} {start}",
        "End": f"{date} {end}",
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
        "FloorLevel": str(floor)
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
    """Test that check_time_overlap correctly prevents bookings within the TIME_GAP buffer."""
    
    global TIME_GAP
    TIME_GAP = 10  # Ensure global variable is set

    # Existing room schedule: Booking from 10:00 AM to 11:00 AM
    room_schedules = {"R1": [(datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 11, 0), None)]}

    # Valid cases: Starts at 11:10 AM (respects the 10-minute gap)
    assert check_time_overlap(sample_group("11:10", "12:00"), sample_room(), room_schedules) is True
    assert check_time_overlap(sample_group("08:10", "09:50"), sample_room(), room_schedules) is True
    # Invalid case: Starts at 10:30 AM, should be rejected due to overlap
    assert check_time_overlap(sample_group("10:30", "11:30"), sample_room(), room_schedules) is False

    # Invalid case: Starts exactly at 11:00 AM (should be rejected due to buffer)
    assert check_time_overlap(sample_group("11:00", "12:00"), sample_room(), room_schedules) is False

    # Invalid case: Fully inside existing booking (10:15 - 10:45)
    assert check_time_overlap(sample_group("10:15", "10:45"), sample_room(), room_schedules) is False

    # Invalid case: Starts before and ends after (9:50 - 11:10) - should be rejected
    assert check_time_overlap(sample_group("09:50", "11:10"), sample_room(), room_schedules) is False

# Unit test for is_valid_assignment
def test_is_valid_assignment():
    room_schedules = {}
    assert is_valid_assignment(sample_group("10:00", "11:00"), sample_room(), room_schedules) is True
    assert is_valid_assignment(sample_group("10:00", "11:00", size=15), sample_room(capacity=10), room_schedules) is False  # Capacity

# Integration tests for backtrack
def test_backtrack_simple_case():
    groups = [sample_group("10:00", "11:00")]
    rooms = [sample_room()]
    result = backtrack(groups, rooms)
    assert len(result) == 1
    assert result[0]["RoomID"] == "R1"

def test_backtrack_conflict():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=False, projector=False, computer=False, floor=1),
        sample_group("11:20", "12:20", size=5, wheelchair=False, projector=False, computer=False, floor=1)
    ]
    rooms = [sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1)]
    
    result = backtrack(groups, rooms)
    
    assert len(result) == 1                      # Only one group should be assigned due to conflict
    assert result[0]["GroupID"] in ["G1", "G2"]  # Ensure at least one group was assigned


def test_backtrack_multiple_rooms():
    groups = [
        sample_group("10:00", "11:00", size=5, wheelchair=True, projector=True, computer=True, floor=1),
        sample_group("10:30", "11:30", size=5, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    rooms = [
        sample_room(room_id="R1", capacity=10, wheelchair=True, projector=True, computer=True, floor=1),
        sample_room(room_id="R2", capacity=10, wheelchair=True, projector=True, computer=True, floor=1)
    ]
    
    result = backtrack(groups, rooms)
    
    assert len(result) == 2  # Both groups should be assigned
    assigned_rooms = {r["RoomID"] for r in result}
    assert "R1" in assigned_rooms and "R2" in assigned_rooms  # Ensure different rooms are used

if __name__ == "__main__":
    pytest.main()
