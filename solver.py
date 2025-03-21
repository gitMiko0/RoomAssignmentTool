from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from data_structs import Group, Room

TIME_GAP = 10  # minutes

def preprocess_data(
    groups: List[Group],
    rooms: List[Room]
) -> Tuple[List[Group], List[Room]]:
    """
    Prepares data for scheduling algorithm
    - Initializes room schedules
    - Converts string timestamps to datetime objects
    - Sorts rooms by capacity
    """
    # Initialize schedules for all rooms
    for room in rooms:
        room['Schedule'] = []
    
    # Convert string times to datetime objects
    for group in groups:
        if isinstance(group['Start'], str):
            group['Start'] = datetime.strptime(group['Start'], "%Y-%m-%d %H:%M")
        if isinstance(group['End'], str):
            group['End'] = datetime.strptime(group['End'], "%Y-%m-%d %H:%M")
    
    return groups, sorted(rooms, key=lambda r: int(r['Capacity']))

def assign_groups(
    groups: List[Group],
    rooms: List[Room],
    index: int = 0
) -> List[Dict[str, str]]:
    """
    Backtracking scheduler with proper state management
    - Uses room.Schedule for bookings
    - Maintains original schedule during backtracking
    """
    if index == len(groups):
        return format_output(rooms)

    group = groups[index]
    
    for room in rooms:
        if is_valid_assignment(group, room):
            # Save current state for potential backtracking
            original_schedule = room['Schedule'].copy()
            room['Schedule'].append((group['Start'], group['End'], group))

            # Recursively assign remaining groups
            result = assign_groups(groups, rooms, index + 1)
            if result:
                return result

            # Backtrack if no solution found
            room['Schedule'] = original_schedule

    return []

def is_valid_assignment(group: Group, room: Room) -> bool:
    """Composite constraint checker with early exit"""
    return all([
        check_floor_preference(group, room),
        check_room_capacity(group, room),
        check_wheelchair_access(group, room),
        check_equipment(group, room),
        check_time_overlap(group, room)
    ])

def check_time_overlap(group: Group, room: Room) -> bool:
    """Time conflict checker using room.Schedule"""
    new_start, new_end = group['Start'], group['End']
    buffer = timedelta(minutes=TIME_GAP)
    
    return not any(
        new_start < (existing_end + buffer) and
        new_end > (existing_start - buffer)
        for existing_start, existing_end, _ in room['Schedule']
    )

def check_equipment(group: Group, room: Room) -> bool:
    """Equipment requirements validation"""
    return (group['Projector'] in ["FALSE", room['Projector']]) and \
           (group['Computer'] in ["FALSE", room['Computer']])

def check_room_capacity(group: Group, room: Room) -> bool:
    """Capacity constraint check"""
    return int(group['Size']) <= int(room['Capacity'])

def check_wheelchair_access(group: Group, room: Room) -> bool:
    """Accessibility requirement check"""
    return group['WheelchairAccess'] == "FALSE" or room['WheelchairAccess'] == "TRUE"

def check_floor_preference(group: Group, room: Room) -> bool:
    """Floor preference validation"""
    return group['FloorPreference'] == "-1" or int(group['FloorPreference']) == int(room['FloorLevel'])

def format_output(rooms: List[Room]) -> List[Dict[str, str]]:
    """Converts schedule to output-ready format"""
    return [
        {
            "GroupID": group['GroupID'],
            "RoomID": room['RoomID'],
            "Start": start.strftime("%H:%M"),
            "End": end.strftime("%H:%M")
        }
        for room in rooms
        for start, end, group in room['Schedule']
    ]
