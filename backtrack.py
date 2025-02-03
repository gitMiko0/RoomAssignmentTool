def can_schedule(room_schedule, new_start, new_end, gap):
    """
    Check if a new booking (new_start to new_end) can be added to the room's schedule,
    ensuring a gap (in minutes) between bookings.
    
    Args:
        room_schedule (list of tuples): Existing bookings as (start, end) in minutes.
        new_start (int): Proposed booking start time (minutes past midnight).
        new_end (int): Proposed booking end time (minutes past midnight).
        gap (int): Required gap (in minutes) between bookings.
        
    Returns:
        bool: True if scheduling is possible; False otherwise.
    """
    for scheduled_start, scheduled_end in room_schedule:
        if new_start < scheduled_end + gap and new_end > scheduled_start - gap:
            return False
    return True

def backtracking_solver(rooms, groups, gap):
    """
    Recursively assigns groups to rooms while satisfying capacity, accessibility,
    equipment, floor preference, and time gap constraints.

    Args:
        rooms (dict): Dictionary of room details.
        groups (list): List of group dictionaries.
        gap (int): Required gap (in minutes) between bookings.
        
    Returns:
        dict or None: Mapping from GroupID to RoomID if assignment found; otherwise, None.
    """
    assignments = {}

    def backtrack(i):
        if i == len(groups):
            return True
        group = groups[i]
        for room_id, room in rooms.items():
            # Constraint: capacity.
            if room["capacity"] < group["size"]:
                continue
            # Constraint: wheelchair access.
            if group["wheelchair"] and not room["wheelchair"]:
                continue
            # Constraint: equipment.
            if group["projector"] and not room["projector"]:
                continue
            if group["computer"] and not room["computer"]:
                continue
            # Constraint: floor preference (if provided, -1 = no preference) .
            if group["floor"] and group["floor"] != room["floor"]:
                continue
            # Constraint: scheduling (time gap).
            if not can_schedule(room["schedule"], group["start"], group["end"], gap):
                continue

            # If all constraints pass, record the assignment.
            assignments[group["id"]] = room_id
            room["schedule"].append((group["start"], group["end"]))

            if backtrack(i + 1):
                return True

            # Backtrack: remove the last assignment and booking.
            assignments.pop(group["id"])
            room["schedule"].pop()
        return False

    return assignments if backtrack(0) else None
