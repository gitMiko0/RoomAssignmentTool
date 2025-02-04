from datetime import datetime, timedelta # For time gap scheduling implementation

TIME_GAP = 10  # Global constant (minutes)

def is_valid_assignment(group, room, assignments):
    """Checks if a group can be assigned to a room while satisfying constraints."""
    group_start = datetime.strptime(group['Start'], "%H:%M")
    group_end = datetime.strptime(group['End'], "%H:%M")

    for assigned in assignments:
        if assigned['RoomID'] == room['RoomID']:
            assigned_start = datetime.strptime(assigned['Start'], "%H:%M")
            assigned_end = datetime.strptime(assigned['End'], "%H:%M")

            # Ensure the group has at least TIME_GAP minutes before and after other bookings
            if not (group_start >= assigned_end + timedelta(minutes=TIME_GAP) or 
                    group_end <= assigned_start - timedelta(minutes=TIME_GAP)):
                return False  # Overlap detected

    return ( # Ensure all constraints are satisfied
        int(group['Size']) <= int(room['Capacity']) and
        (room['WheelchairAccess'] == "TRUE" or group['WheelchairAccess'] == "FALSE") and
        (room['Projector'] == "TRUE" or group['Projector'] == "FALSE") and
        (room['Computer'] == "TRUE" or group['Computer'] == "FALSE") and
        (int(group['FloorPreference']) == -1 or int(group['FloorPreference']) == int(room['FloorLevel']))  # -1 means no preference
    )

def backtrack(groups, rooms, assignments=[], index=0):
    """Recursive backtracking function to assign groups to rooms."""
    if index == len(groups):
        return assignments  # All groups assigned successfully

    group = groups[index]
    for room in rooms:
        if is_valid_assignment(group, room, assignments):
            assignments.append({
                "GroupID": group['GroupID'], 
                "RoomID": room['RoomID'], 
                "Start": group['Start'], 
                "End": group['End']
            })

            result = backtrack(groups, rooms, assignments, index + 1)
            if result:
                return result  # Found a valid assignment

            assignments.pop()  # Backtrack

    return None  # No valid assignment found
