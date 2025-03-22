from typing import TypedDict, List, Dict, Tuple
from datetime import datetime, timedelta
from data_structs import Group, Room

TIME_GAP = 10 
# In minutes. Valid schedules must have this minimum gap.
# The tool does NOT modify existing schedule requests, the input is expected to consider this gap in order to be valid.

# ================= Core Logic =================
def preprocess_data(
    raw_groups: List[Dict], 
    raw_rooms: List[Dict]
) -> Tuple[List[Group], List[Room]]:
    """Convert raw string data to properly typed structures, this is an efficiency choice
        to avoid repeated conversions in the main algorithm as well as to have a place to sort
        the rooms by capacity before the algorithm receives the data."""
    groups = []
    for rg in raw_groups:
        group: Group = {
            'GroupID':              rg['GroupID'],
            # Datetime Object conversion -> datetime.strptime("2023-03-21 10:00", "%Y-%m-%d %H:%M")
            # Returns: datetime.datetime(2023, 3, 21, 10, 0)
            'Start':                datetime.strptime(rg['Start'], "%Y-%m-%d %H:%M"),
            'End':                  datetime.strptime(rg['End'], "%Y-%m-%d %H:%M"),
            'Size':                 int(rg['Size']),
            'WheelchairAccess':     rg['WheelchairAccess'].upper() == 'TRUE',
            'Projector':            rg['Projector'].upper() == 'TRUE',
            'Computer':             rg['Computer'].upper() == 'TRUE',
            'FloorPreference':      int(rg['FloorPreference'])
        }
        groups.append(group)

    rooms = []
    for rr in raw_rooms:
        room: Room = {
            'RoomID': rr['RoomID'],
            'Capacity': int(rr['Capacity']),
            'WheelchairAccess': rr['WheelchairAccess'].upper() == 'TRUE',
            'Projector': rr['Projector'].upper() == 'TRUE',
            'Computer': rr['Computer'].upper() == 'TRUE',
            'FloorLevel': int(rr['FloorLevel']),
            # Schedule is filled in the main algorithm as it assigns groups
            'Schedule': []
        }
        rooms.append(room)

    return groups, sorted(rooms, key=lambda r: r['Capacity'])

def assign_groups(
    groups: List[Group],
    rooms: List[Room],
    index: int = 0
) -> List[Dict[str, str]]:
    """Backtracking scheduler with proper state management"""
    if index == len(groups):
        return format_output(rooms)

    group = groups[index]
    
    for room in rooms:
        if is_valid_assignment(group, room):
            # Save state for backtracking
            original_schedule = room['Schedule'].copy()
            room['Schedule'].append((group['Start'], group['End'], group))

            result = assign_groups(groups, rooms, index + 1)
            if result:
                return result

            # Restore original schedule
            room['Schedule'] = original_schedule

    return []

# ================= Constraint Checks =================
def is_valid_assignment(group: Group, room: Room) -> bool:
    """Composite constraint check"""
    return all([
        check_floor_preference(group, room),
        check_room_capacity(group, room),
        check_wheelchair_access(group, room),
        check_equipment(group, room),
        check_time_overlap(group, room)
    ])

def check_time_overlap(group: Group, room: Room) -> bool:
    """Check if group timing conflicts with existing room schedule (including buffer)"""
    buffer = timedelta(minutes=TIME_GAP)
    new_start = group['Start']
    new_end = group['End']
    
    # Check against all existing bookings in the room
    for existing_start, existing_end, _ in room['Schedule']:
        # Apply buffer to existing booking's time range
        existing_start_buffered = existing_start - buffer
        existing_end_buffered = existing_end + buffer
        
        # Check if new booking overlaps with buffered existing booking
        if (new_start < existing_end_buffered) and (new_end > existing_start_buffered):
            return False  # Conflict found
    
    return True  # No conflicts found


def check_equipment(group: Group, room: Room) -> bool:
    """Equipment requirements check"""
    # Group only needs what it explicitly requires
    return (not group['Projector'] or room['Projector']) and \
           (not group['Computer'] or room['Computer'])

def check_room_capacity(group: Group, room: Room) -> bool:
    """Capacity constraint check"""
    return group['Size'] <= room['Capacity']

def check_wheelchair_access(group: Group, room: Room) -> bool:
    """Accessibility requirement check"""
    return not group['WheelchairAccess'] or room['WheelchairAccess']

def check_floor_preference(group: Group, room: Room) -> bool:
    """Floor preference validation"""
    return group['FloorPreference'] == -1 or group['FloorPreference'] == room['FloorLevel']

# ================= Output Formatting =================
def format_output(rooms: List[Room]) -> List[Dict[str, str]]:
    """Convert schedule to output format"""
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
