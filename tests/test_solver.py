"""
Module Name: test_solver.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Black-box tests for the Room Assignment Tool’s solver logic,
verifying successful, backtracking, and failure scenarios.
"""

from src.solver import assign_groups
from test_helper import sample_group, sample_room

def test_solver_valid_single_assignment():
    groups = [sample_group("10:00", "11:00", group_id="G1")]
    rooms = [sample_room(room_id="R1")]
    result = assign_groups(groups, rooms, time_gap=10)
    assert result is not None
    assert any(r.schedule for r in result)

def test_solver_backtracking_needed():
    groups = [
        sample_group("10:00", "11:00", group_id="G1"),
        sample_group("10:30", "11:30", group_id="G2")
    ]
    rooms = [
        sample_room(room_id="R1"),
        sample_room(room_id="R2")
    ]
    result = assign_groups(groups, rooms, time_gap=10)
    assert result is not None
    assigned = [room for room in result if room.schedule]
    assert len(assigned) == 2

def test_solver_unsatisfiable_input():
    groups = [
        sample_group("10:00", "11:00", group_id="G1", size=50),
        sample_group("11:30", "12:30", group_id="G2", size=50)
    ]
    rooms = [
        sample_room(room_id="R1", capacity=10)
    ]
    result = assign_groups(groups, rooms, time_gap=10)
    assert result is None
