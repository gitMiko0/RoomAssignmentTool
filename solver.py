import sys
from input_reader import read_csv
from output_writer import write_output
from datetime import datetime, timedelta

TIME_GAP = 10  # Global constant (minutes)

def backtrack(groups, rooms, room_schedules=None, index=0):
    if room_schedules is None:
        room_schedules = {}  # Avoid mutable default argument issue
    
    if index == len(groups):
        return [{"GroupID": g['GroupID'], "RoomID": r, "Start": s.strftime("%H:%M"), "End": e.strftime("%H:%M")}
                for r, schedule in room_schedules.items() for s, e, g in schedule]

    group = groups[index]
    
    for room in sorted(rooms, key=lambda r: int(r['Capacity'])):
        if is_valid_assignment(group, room, room_schedules):
            # Copy the room schedule before modification
            if room['RoomID'] not in room_schedules:
                room_schedules[room['RoomID']] = []

            # Convert times properly
            start_time = datetime.strptime(group['Start'], "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(group['End'], "%Y-%m-%d %H:%M")
            
            # Assign group
            room_schedules[room['RoomID']].append((start_time, end_time, group))
            
            # Debugging output
            print(f"Assigned {group['GroupID']} to {room['RoomID']} at {group['Start']} - {group['End']}")

            # Recurse with updated schedules
            result = backtrack(groups, rooms, room_schedules, index + 1)
            if result:
                return result

            # Undo assignment if backtracking
            room_schedules[room['RoomID']].pop()
            print(f"Backtracking: Removed {group['GroupID']} from {room['RoomID']}")

    return []

def is_valid_assignment(group, room, room_schedules):
    """Checks if a group can be assigned to a room while satisfying all constraints."""
    return (
        check_floor_preference(group, room) and         # 1. Floor preference check
        check_room_capacity(group, room) and            # 2. Room capacity check
        check_wheelchair_access(group, room) and        # 3. Wheelchair access check
        check_equipment(group, room) and                # 4. Equipment check
        check_time_overlap(group, room, room_schedules) # 5. Room-specific Time check, Only check when all other constraints are good!
    )

def check_time_overlap(group, room, room_schedules):
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
    """Checks if the room satisfies the group's projector and computer needs."""
    return (group['Projector'] == "FALSE" or room['Projector'] == "TRUE") and \
           (group['Computer'] == "FALSE" or room['Computer'] == "TRUE")

def check_room_capacity(group, room):
    """Checks if the room can accommodate the group's size."""
    return int(group['Size']) <= int(room['Capacity'])

def check_wheelchair_access(group, room):
    """Checks if the group and room's wheelchair access are compatible."""
    return group['WheelchairAccess'] == "FALSE" or room['WheelchairAccess'] == "TRUE"

def check_floor_preference(group, room):
    """Checks if the room satisfies the group's floor preference."""
    return group['FloorPreference'] == "-1" or int(group['FloorPreference']) == int(room['FloorLevel'])