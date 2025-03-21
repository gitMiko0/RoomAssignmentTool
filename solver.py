from typing import TypedDict, Literal, List, Dict, Tuple
from datetime import datetime, timedelta
import sys
from input_reader import read_csv
from output_writer import write_output
from data_structs import Group, Room

TIME_GAP = 10  # Global constant (minutes)

def preprocess_data(
    groups: List[Group],
    rooms: List[Room]
) -> Tuple[List[Group], List[Room]]:
    """Prepares data for scheduling algorithm"""
    # Type conversion for datetime fields
    for group in groups:
        if isinstance(group['Start'], str):
            group['Start'] = datetime.strptime(group['Start'], "%Y-%m-%d %H:%M")
        if isinstance(group['End'], str):
            group['End'] = datetime.strptime(group['End'], "%Y-%m-%d %H:%M")
    
    return groups, sorted(rooms, key=lambda r: int(r['Capacity']))

def assign_groups(
    groups: List[Group],
    rooms: List[Room],
    room_schedules: Dict[str, List[Tuple[datetime, datetime, Group]]] = None,
    index: int = 0
) -> List[Dict[str, str]]:
    """Core scheduling algorithm with backtracking"""
    room_schedules = room_schedules or {}
    
    if index == len(groups):
        return format_output(room_schedules)

    group = groups[index]
    
    for room in rooms:  # Rooms are pre-sorted
        if is_valid_assignment(group, room, room_schedules):
            room_id = room['RoomID']
            room_schedules.setdefault(room_id, []).append(
                (group['Start'], group['End'], group)
            )

            if result := assign_groups(groups, rooms, room_schedules, index + 1):
                return result

            room_schedules[room_id].pop()  # Backtrack

    return []

def format_output(schedules: Dict[str, List[Tuple[datetime, datetime, Group]]]) -> List[Dict[str, str]]:
    """Converts final schedule to output format"""
    return [{
        "GroupID": g['GroupID'],
        "RoomID": room_id,
        "Start": s.strftime("%H:%M"),
        "End": e.strftime("%H:%M")
    } for room_id, bookings in schedules.items() for s, e, g in bookings]

# Constraint checking functions remain unchanged but now use typed parameters
def is_valid_assignment(group: Group, room: Room, room_schedules: Dict[str, List[Tuple[datetime, datetime, Group]]]) -> bool:
    return all([
        check_floor_preference(group, room),
        check_room_capacity(group, room),
        check_wheelchair_access(group, room),
        check_equipment(group, room),
        check_time_overlap(group, room, room_schedules)
    ])

def check_time_overlap(group: Group, room: Room, room_schedules: Dict[str, List[Tuple[datetime, datetime, Group]]]) -> bool:
    if room['RoomID'] not in room_schedules:
        return True

    new_start, new_end = group['Start'], group['End']
    buffer = timedelta(minutes=TIME_GAP)
    
    return not any(
        new_start < (existing_end + buffer) and
        new_end > (existing_start - buffer)
        for existing_start, existing_end, _ in room_schedules[room['RoomID']]
    )

# Other constraint functions remain type-annotated but otherwise unchanged


def check_equipment(group, room):
    """Checks if the room meets the group's equipment requirements."""
    return (group['Projector'] == "FALSE" or room['Projector'] == "TRUE") and \
           (group['Computer'] == "FALSE" or room['Computer'] == "TRUE")

def check_room_capacity(group, room):
    """Verifies if the room has enough capacity for the group size."""
    return int(group['Size']) <= int(room['Capacity'])

def check_wheelchair_access(group, room):
    """Ensures that wheelchair accessibility requirements are met."""
    return group['WheelchairAccess'] == "FALSE" or room['WheelchairAccess'] == "TRUE"

def check_floor_preference(group, room):
    """Confirms if the room is on the preferred floor."""
    return group['FloorPreference'] == "-1" or int(group['FloorPreference']) == int(room['FloorLevel'])