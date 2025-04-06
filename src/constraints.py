"""
Module Name: constraints.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Defines all constraint-checking logic used to validate whether a group
can be assigned to a given room based on equipment, capacity, accessibility,
schedule conflicts, and floor preference.
"""

from datetime import timedelta
from .group import Group
from .room import Room

def is_valid_assignment(group: Group, room: Room, time_gap: int) -> bool:
    """
    is_valid_assignment
        Combines all constraint checks into a single validation call.

    Parameters:
        group (Group) - The group being assigned.
        room (Room) - The room being considered for assignment.
        time_gap (int) - The buffer (in minutes) between group schedules.

    Return Value:
        bool - True if all constraints pass; otherwise, False.
    """
    return all([
        check_floor_preference(group, room),
        check_room_capacity(group, room),
        check_wheelchair_access(group, room),
        check_equipment(group, room),
        check_time_overlap(group, room, time_gap)
    ])

def check_time_overlap(group: Group, room: Room, time_gap: int) -> bool:
    """
    check_time_overlap
        Ensures no schedule conflicts exist for the room, including a time buffer.

    Parameters:
        group (Group) - The group to be scheduled.
        room (Room) - The room with current bookings.
        time_gap (int) - The buffer in minutes between bookings.

    Return Value:
        bool - True if there is no overlap; otherwise, False.
    """
    buffer = timedelta(minutes=time_gap)
    new_start = group.start
    new_end = group.end

    for existing_start, existing_end, _ in room.schedule:
        if (new_start < existing_end + buffer) and (new_end > existing_start - buffer):
            return False
    return True

def check_floor_preference(group: Group, room: Room) -> bool:
    """
    check_floor_preference
        Matches the group’s preferred floor to the room’s floor.

    Parameters:
        group (Group) - The group requesting a floor.
        room (Room) - The room being checked.

    Return Value:
        bool - True if the room satisfies the floor preference.
    """
    return group.floor_preference == -1 or group.floor_preference == room.floor_level

def check_room_capacity(group: Group, room: Room) -> bool:
    """
    check_room_capacity
        Verifies the room can hold the group size.

    Parameters:
        group (Group) - The group with a size requirement.
        room (Room) - The room being evaluated.

    Return Value:
        bool - True if the room capacity meets or exceeds the group size.
    """
    return group.size <= room.capacity

def check_wheelchair_access(group: Group, room: Room) -> bool:
    """
    check_wheelchair_access
        Confirms that the room meets the group’s accessibility needs.

    Parameters:
        group (Group) - The group which may require accessibility.
        room (Room) - The room being validated.

    Return Value:
        bool - True if accessible or not required.
    """
    return not group.wheelchair_access or room.wheelchair_access

def check_equipment(group: Group, room: Room) -> bool:
    """
    check_equipment
        Validates the room has all equipment the group requires.

    Parameters:
        group (Group) - The group with equipment needs.
        room (Room) - The candidate room.

    Return Value:
        bool - True if all required equipment is present.
    """
    return (not group.projector or room.projector) and \
           (not group.computer or room.computer)

