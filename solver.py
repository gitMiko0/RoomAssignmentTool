import sys
from input_reader import read_csv
from output_writer import write_output
from datetime import datetime, timedelta

TIME_GAP = 10  # Global constant (minutes)

def assign_groups(groups, rooms, room_schedules=None, index=0):
    """
    Recursively assigns groups to rooms using backtracking to find a valid schedule.
    
    Parameters:
        groups (list): List of group dictionaries containing scheduling information.
        rooms (list): List of room dictionaries containing capacity and equipment details.
        room_schedules (dict): Tracks current room assignments.
        index (int): Current group index being processed.
    
    Returns:
        list: A list of valid room assignments if successful, otherwise an empty list.
    """
    if room_schedules is None:
        room_schedules = {}
    
    if index == len(groups):
        return [{"GroupID": g['GroupID'], "RoomID": r, "Start": s.strftime("%H:%M"), "End": e.strftime("%H:%M")}
                for r, schedule in room_schedules.items() for s, e, g in schedule]

    group = groups[index]
    
    for room in sorted(rooms, key=lambda r: int(r['Capacity'])):
        if is_valid_assignment(group, room, room_schedules):
            if room['RoomID'] not in room_schedules:
                room_schedules[room['RoomID']] = []

            start_time = datetime.strptime(group['Start'], "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(group['End'], "%Y-%m-%d %H:%M")
            
            room_schedules[room['RoomID']].append((start_time, end_time, group))
            print(f"Assigned {group['GroupID']} to {room['RoomID']} at {group['Start']} - {group['End']}")

            result = assign_groups(groups, rooms, room_schedules, index + 1)
            if result:
                return result

            room_schedules[room['RoomID']].pop()
            print(f"Backtracking: Removed {group['GroupID']} from {room['RoomID']}")

    return []

def is_valid_assignment(group, room, room_schedules):
    """
    Checks if assigning a group to a room meets all constraints.
    
    Parameters:
        group (dict): The group attempting to book a room.
        room (dict): The room being considered.
        room_schedules (dict): Existing room assignments.
    
    Returns:
        bool: True if the room satisfies all constraints, otherwise False.
    """
    return (
        check_floor_preference(group, room) and
        check_room_capacity(group, room) and
        check_wheelchair_access(group, room) and
        check_equipment(group, room) and
        check_time_overlap(group, room, room_schedules)
    )

def check_time_overlap(group, room, room_schedules):
    """
    Ensures that a new booking does not overlap with existing bookings.
    
    Parameters:
        group (dict): The group attempting to book a room.
        room (dict): The room being checked.
        room_schedules (dict): Existing room assignments.
    
    Returns:
        bool: True if there is no scheduling conflict, otherwise False.
    """
    room_id = room["RoomID"]
    
    if room_id not in room_schedules:
        print(f"Room {room_id} is empty, allowing booking for {group['Start']} - {group['End']}")
        return True

    new_start = datetime.strptime(group["Start"], "%Y-%m-%d %H:%M")
    new_end = datetime.strptime(group["End"], "%Y-%m-%d %H:%M")

    BUFFER = timedelta(minutes=TIME_GAP)

    print(f"Checking {room_id} for overlap with {group['Start']} - {group['End']}")
    
    for booked_start, booked_end, _ in room_schedules[room_id]:
        adjusted_start = booked_start - BUFFER
        adjusted_end = booked_end + BUFFER

        print(f"Existing: {booked_start.strftime('%Y-%m-%d %H:%M')} - {booked_end.strftime('%Y-%m-%d %H:%M')}, Adjusted: {adjusted_start.strftime('%Y-%m-%d %H:%M')} - {adjusted_end.strftime('%Y-%m-%d %H:%M')}")

        if new_start < adjusted_end and new_end > adjusted_start:
            print("Conflict detected! Rejecting booking.")
            return False
    
    print("No conflict, booking allowed.")
    return True

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