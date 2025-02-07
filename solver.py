import sys
from input_reader import read_csv
from output_writer import write_output
from datetime import datetime, timedelta

TIME_GAP = 10  # Global constant (minutes)

def backtrack(groups, rooms, room_schedules={}, index=0):
    """Recursive backtracking function to assign groups to rooms."""
    if index == len(groups):  # All groups assigned
        return [{"GroupID": g['GroupID'], "RoomID": r, "Start": s.strftime("%H:%M"), "End": e.strftime("%H:%M")} 
                for r, schedule in room_schedules.items() for s, e, g in schedule]
    
    group = groups[index]
    
    # Sort rooms based on best fit (smallest room that fits the group)
    sorted_rooms = sorted(rooms, key=lambda r: int(r['Capacity']))
    
    for room in sorted_rooms:
        if not check_floor_preference(group, room):
            continue  # Skip if the floor preference is not met
        
        if is_valid_assignment(group, room, room_schedules):
            if room['RoomID'] not in room_schedules:
                room_schedules[room['RoomID']] = []
            
            room_schedules[room['RoomID']].append((
                datetime.strptime(group['Start'], "%H:%M"), 
                datetime.strptime(group['End'], "%H:%M"),
                group
            ))
            
            result = backtrack(groups, rooms, room_schedules, index + 1)
            if result:  # If a valid assignment is found
                return result  
            
            room_schedules[room['RoomID']].pop()  # Backtrack if no valid assignment found
    
    return []  # Return an empty list if no valid assignment is possible

def check_time_overlap(group, room, room_schedules):
    """Checks if the group's time overlaps with any existing assignments in the same room."""
    group_start = datetime.strptime(group['Start'], "%H:%M")
    group_end = datetime.strptime(group['End'], "%H:%M")
    
    if room['RoomID'] not in room_schedules:
        return True  # No conflicts if no prior assignments in the room
    
    for assigned_start, assigned_end, _ in room_schedules[room['RoomID']]:  # Fixed unpacking issue
        if not (group_start >= assigned_end + timedelta(minutes=TIME_GAP) or 
                group_end <= assigned_start - timedelta(minutes=TIME_GAP)):
            return False  # Overlap detected
    
    return True  # No overlap

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

def is_valid_assignment(group, room, room_schedules):
    """Checks if a group can be assigned to a room while satisfying all constraints."""
    return (
        check_floor_preference(group, room) and         # Floor preference check
        check_room_capacity(group, room) and            # Room capacity check
        check_wheelchair_access(group, room) and        # Wheelchair access check
        check_equipment(group, room) and                # Equipment check
        check_time_overlap(group, room, room_schedules) # Room-specific Time check
    )