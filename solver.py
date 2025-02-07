from datetime import datetime, timedelta

TIME_GAP = 10  # Global constant (minutes)

def check_time_overlap(group, room, assignments):
    """Checks if the group's time overlaps with any existing assignments in the room."""
    group_start = datetime.strptime(group['Start'], "%H:%M")
    group_end = datetime.strptime(group['End'], "%H:%M")

    # If no previous assignments, there's no time conflict.
    if not assignments:
        print(f"No previous assignments. Group {group['GroupID']} can be assigned.")
        return True
    
    for assigned in assignments:
        if assigned['RoomID'] == room['RoomID']:
            assigned_start = datetime.strptime(assigned['Start'], "%H:%M")
            assigned_end = datetime.strptime(assigned['End'], "%H:%M")

            # Ensure there is a time gap between the assignments
            # A gap of `TIME_GAP` minutes is required between the end of one group and the start of the next
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

def is_valid_assignment(group, room, assignments):
    """Checks if a group can be assigned to a room while satisfying all constraints."""
    return (
        check_floor_preference(group, room) and         # Floor preference check
        check_room_capacity(group, room) and            # Room capacity check
        check_wheelchair_access(group, room) and        # Wheelchair access check
        check_equipment(group, room)                    # Equipment check
        # check_time_overlap(group, room, assignments)    # Time check (last since it's costly)
    )


def backtrack(groups, rooms, assignments=[], index=0):
    """Recursive backtracking function to assign groups to rooms."""
    if index == len(groups):  # All groups assigned
        return assignments  # Return the assignments once all groups are processed
    
    group = groups[index]

    # Sort rooms based on best fit (smallest room that fits the group)
    sorted_rooms = sorted(rooms, key=lambda r: int(r['Capacity']))

    for room in sorted_rooms:
        if not check_floor_preference(group, room):
            continue  # Skip if the floor preference is not met
        
        if is_valid_assignment(group, room, assignments):
            assignments.append({
                "GroupID": group['GroupID'], 
                "RoomID": room['RoomID'], 
                "Start": group['Start'], 
                "End": group['End']
            })

            result = backtrack(groups, rooms, assignments, index + 1)
            if result:  # If a valid assignment is found
                return result  

            assignments.pop()  # Backtrack if no valid assignment found

    return []  # Return an empty list if no valid assignment is possible
