"""
Module Name: test_constraints.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Unit tests for individual constraint-checking functions.
"""

from datetime import datetime
from test_helper import sample_group, sample_room
from src.constraints import (
    check_floor_preference, check_room_capacity, check_wheelchair_access,
    check_equipment, check_time_overlap, is_valid_assignment
)
from src.room import Room
from src.group import Group

# === Constraint Tests ===
def test_check_floor_preference():
    assert check_floor_preference(sample_group("10:00", "11:00", floor=-1), sample_room(floor=2)) is True
    assert check_floor_preference(sample_group("10:00", "11:00", floor=2), sample_room(floor=2)) is True
    assert check_floor_preference(sample_group("10:00", "11:00", floor=3), sample_room(floor=2)) is False

def test_check_room_capacity():
    assert check_room_capacity(sample_group("10:00", "11:00", size=10), sample_room(capacity=10)) is True
    assert check_room_capacity(sample_group("10:00", "11:00", size=11), sample_room(capacity=10)) is False

def test_check_wheelchair_access():
    assert check_wheelchair_access(sample_group("10:00", "11:00", wheelchair=True), sample_room(wheelchair=True)) is True
    assert check_wheelchair_access(sample_group("10:00", "11:00", wheelchair=True), sample_room(wheelchair=False)) is False

def test_check_equipment():
    assert check_equipment(sample_group("10:00", "11:00", projector=True, computer=True), sample_room()) is True
    assert check_equipment(sample_group("10:00", "11:00", projector=True, computer=False), sample_room(projector=False)) is False

def test_check_time_overlap():
    room = sample_room()
    existing_group = sample_group("10:00", "11:00")
    room.add_booking(existing_group.start, existing_group.end, existing_group)

    assert check_time_overlap(sample_group("11:10", "12:00"), room, time_gap=10)
    assert not check_time_overlap(sample_group("10:30", "11:30"), room, time_gap=10)

def test_valid_assignment_all_conditions_pass():
    group = sample_group("10:00", "11:00", size=5, wheelchair=True, projector=True, computer=True, floor=1)
    room = sample_room(capacity=10, wheelchair=True, projector=True, computer=True, floor=1)
    assert is_valid_assignment(group, room, time_gap=10)

def test_invalid_assignment_due_to_capacity():
    group = sample_group("10:00", "11:00", size=20)
    room = sample_room(capacity=10)
    assert not is_valid_assignment(group, room, time_gap=10)

def test_invalid_assignment_due_to_floor_preference():
    group = sample_group("10:00", "11:00", floor=2)
    room = sample_room(floor=1)
    assert not is_valid_assignment(group, room, time_gap=10)

def test_invalid_assignment_due_to_equipment():
    group = sample_group("10:00", "11:00", projector=True, computer=True)
    room = sample_room(projector=False, computer=True)
    assert not is_valid_assignment(group, room, time_gap=10)

def test_invalid_assignment_due_to_wheelchair():
    group = sample_group("10:00", "11:00", wheelchair=True)
    room = sample_room(wheelchair=False)
    assert not is_valid_assignment(group, room, time_gap=10)

def test_invalid_assignment_due_to_time_conflict():
    group1 = sample_group("10:00", "11:00", group_id="G1")
    group2 = sample_group("10:30", "11:30", group_id="G2")
    room = sample_room()
    room.add_booking(group1.start, group1.end, group1)
    assert not is_valid_assignment(group2, room, time_gap=10)
