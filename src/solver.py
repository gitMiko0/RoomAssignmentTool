"""
Module Name: solver.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Provides the core backtracking logic and preprocessing functions for assigning groups to rooms
based on constraints such as schedule, equipment, accessibility, and room capacity.
"""

from typing import List, Dict, Optional
from .group import Group
from .room import Room
from .constraints import is_valid_assignment
from datetime import datetime

"""
Module Summary:
This module handles the core backtracking algorithm and data preparation logic for the Room Assignment Tool.
It includes:
- `preprocess_data`: Converts raw dictionary input into typed `Group` and `Room` objects.
- `assign_groups`: Recursive function using backtracking to assign each group to a valid room.
- `format_output`: Prepares the final assignments in a structured output format.

Dependencies:
- `group.py`: Defines the Group data structure.
- `room.py`: Defines the Room data structure and its scheduling methods.
- `constraints.py`: Contains all constraint-checking functions.

Known/Suspected Errors:
- Does not currently optimize for room utilization (greedy approach).
"""

def assign_groups(groups: List[Group], rooms: List[Room], time_gap: int, index: int = 0) -> Optional[List[Room]]:
    """
    assign_groups
        Recursively assigns each group to a valid room using backtracking and constraint validation.

    Parameters:
        groups (List[Group]) - List of all group objects to assign
        rooms (List[Room]) - List of available room objects (modified in-place)
        time_gap (int) - Minimum time gap (in minutes) required between group schedules
        index (int) - Internal index tracker used by the recursive call

    Return Value:
        Optional[List[Room]] - Returns the modified list of rooms if a complete assignment is possible,
                               otherwise returns None.
    """
    if index == len(groups):
        return rooms  # All groups assigned successfully

    group = groups[index]
    # print(f"[Info] Attempting to assign group {group.id} (Index {index})") -- uncomment for inspection

    for room in rooms:
        if is_valid_assignment(group, room, time_gap):
            room.add_booking(group.start, group.end, group)
            result = assign_groups(groups, rooms, time_gap, index + 1)
            if result is not None:
                return result
            room.remove_last_booking()
            print(f"[Backtrack] Removed group {group.id} from room {room.id}")

    return None  # No valid assignment found for this group

def format_output(rooms: List[Room]) -> List[Dict[str, str]]:
    """
    format_output
        Formats the final room assignments into a dictionary format for file writing or console output.

    Parameters:
        rooms (List[Room]) - List of rooms, each containing schedule data with assigned groups

    Return Value:
        List[Dict[str, str]] - List of dictionaries containing GroupID, RoomID, Start and End time strings
    """
    return [
        {
            "GroupID": group.id,
            "RoomID": room.id,
            "Start": start.strftime("%H:%M"),
            "End": end.strftime("%H:%M")
        }
        for room in rooms
        for start, end, group in room.schedule
    ]
