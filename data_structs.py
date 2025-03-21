from typing import TypedDict, Literal, List, Dict, Tuple
from datetime import datetime


class Group(TypedDict):
    GroupID: str
    Start: datetime
    End: datetime
    Size: str
    WheelchairAccess: Literal["TRUE", "FALSE"]
    Projector:        Literal["TRUE", "FALSE"]
    Computer:         Literal["TRUE", "FALSE"]
    FloorPreference: str

class Room(TypedDict):
    RoomID: str
    Capacity: str
    WheelchairAccess: Literal["TRUE", "FALSE"]
    Projector:        Literal["TRUE", "FALSE"]
    Computer:         Literal["TRUE", "FALSE"]
    FloorLevel: str
    Schedule: List[Tuple[datetime, datetime, Group]]
