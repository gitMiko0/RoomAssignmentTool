# constraints.py
from datetime import timedelta
from group import Group
from room import Room

def is_valid_assignment(group: Group, room: Room, time_gap: int) -> bool:
    """Composite check to ensure the room can host the group."""
    return all([
        check_floor_preference(group, room),
        check_room_capacity(group, room),
        check_wheelchair_access(group, room),
        check_equipment(group, room),
        check_time_overlap(group, room, time_gap)
    ])

def check_time_overlap(group: Group, room: Room, time_gap: int) -> bool:
    """
    Prevents overlapping schedules in the same room.
    A buffer defined by `time_gap` (in minutes) is added before and after each existing booking
    to ensure spacing between events. A new group cannot overlap within that buffer zone.
    """
    buffer = timedelta(minutes=time_gap)
    new_start = group.start
    new_end = group.end

    for existing_start, existing_end, _ in room.schedule:
        # Extend existing booking with buffer
        if (new_start < existing_end + buffer) and (new_end > existing_start - buffer):
            return False  # Overlap within the buffer zone
    return True

def check_floor_preference(group: Group, room: Room) -> bool:
    """
    If the group has no preference (indicated by -1), any floor is accepted.
    Otherwise, the room must exactly match the requested floor.
    """
    return group.floor_preference == -1 or group.floor_preference == room.floor_level

def check_room_capacity(group: Group, room: Room) -> bool:
    """
    Room must accommodate at least the size of the group.
    No partial assignments allowed.
    """
    return group.size <= room.capacity

def check_wheelchair_access(group: Group, room: Room) -> bool:
    """
    If the group requires wheelchair access, the room must have it.
    Otherwise, accessibility doesn't matter.
    """
    return not group.wheelchair_access or room.wheelchair_access

def check_equipment(group: Group, room: Room) -> bool:
    """
    A room is valid if it satisfies all of the group's required equipment.
    If a requirement is False, that equipment is not needed.
    """
    return (not group.projector or room.projector) and \
           (not group.computer or room.computer)
