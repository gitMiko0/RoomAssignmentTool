from typing import List, Dict, Optional
from .group import Group
from .room import Room
from .constraints import is_valid_assignment
from datetime import datetime

def preprocess_data(raw_groups: List[Dict], raw_rooms: List[Dict]) -> tuple[list[Group], list[Room]]:
    """Converts dictionaries into structured Group and Room objects, sorting rooms and groups."""
    # Sort groups to try earlier + bigger ones first (helps with pruning)
    groups = sorted([Group.from_dict(g) for g in raw_groups], key=lambda g: (g.start, -g.size))
    rooms = sorted([Room.from_dict(r) for r in raw_rooms], key=lambda r: r.capacity)
    return groups, rooms

def assign_groups(groups: List[Group], rooms: List[Room], time_gap: int, index: int = 0) -> Optional[List[Room]]:
    if index == len(groups):
        return rooms  # All groups assigned successfully

    group = groups[index]
    print(f"[Info] Attempting to assign group {group.id} (Index {index})")

    for room in rooms:
        if is_valid_assignment(group, room, time_gap):
            room.add_booking(group.start, group.end, group)
            result = assign_groups(groups, rooms, time_gap, index + 1)
            if result is not None:
                return result
            room.remove_last_booking()
            print(f"[Backtrack] Removed group {group.id} from room {room.id}")

    return None  # No valid assignment found for this group


def format_output(rooms: List[Room]) -> List[Dict[str, str]]:
    """Formats the final schedule into a list of dictionaries suitable for output."""
    return [
        {
            "GroupID": group.id,
            "RoomID": room.id,
            "Start": start.strftime("%H:%M"),
            "End": end.strftime("%H:%M")
        }
        for room in rooms
        for start, end, group in room.schedule
    ]
