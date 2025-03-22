from typing import TypedDict, List, Tuple
from datetime import datetime

# ================= Data Structures =================
class Group(TypedDict):
    GroupID:            str
    Start:              datetime
    End:                datetime
    Size:               int
    WheelchairAccess:   bool
    Projector:          bool
    Computer:           bool
    FloorPreference:    int

class Room(TypedDict):
    RoomID:             str
    Capacity:           int
    WheelchairAccess:   bool
    Projector:          bool
    Computer:           bool
    FloorLevel:         int
    Schedule:           List[Tuple[datetime, datetime, Group]]