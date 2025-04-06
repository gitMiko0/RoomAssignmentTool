"""
Module Name: input_reader.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Handles CLI interface and CSV parsing. Converts and validates all input into structured Group and Room objects.

Module Summary:
This module provides high-level input processing and validation logic. It handles CLI parsing, CSV loading,
conversion of raw CSV entries into valid `Group` and `Room` objects, and provides safety-checked defaults.
All validation logic is self-contained, and errors are raised or reported in a user-friendly manner.

Key Functions:
- load_and_prepare_input: Top-level data entry function, handles CLI + preprocessing
- preprocess_data: Validates and converts raw input dictionaries
- read_csv: Loads CSV into dictionaries
- parse_bool, parse_int, parse_time: Field validation helpers

Dependencies:
- group.py, room.py
- csv, datetime, sys

Known/Suspected Errors:
- None known at this time.
"""

import csv
import sys
from datetime import datetime
from typing import List, Dict
from .group import Group
from .room import Room
from .validators import parse_bool, parse_int, parse_time

DEFAULT_TIME_GAP = 10  # in minutes

def load_and_prepare_input() -> tuple[list[Group], list[Room], int]:
    """
    load_and_prepare_input
        Handles full pipeline: CLI args, CSV loading, validation, and conversion into objects.

    Return Value:
        tuple[list[Group], list[Room], int] - groups, rooms, time_gap (minutes)

    Exceptions:
        SystemExit - On any parsing or validation error
    """
    try:
        args = sys.argv[1:]
        if len(args) < 2:
            raise ValueError("Usage: <rooms_file.csv> <groups_file.csv> [time_gap_minutes]")

        rooms_file = args[0]
        groups_file = args[1]
        time_gap = int(args[2]) if len(args) >= 3 else DEFAULT_TIME_GAP

        raw_rooms = read_csv(rooms_file)
        raw_groups = read_csv(groups_file)

        groups, rooms = preprocess_data(raw_groups, raw_rooms)
        return groups, rooms, time_gap

    except ValueError as e:
        print("Error:", e)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def read_csv(filename: str) -> List[Dict[str, str]]:
    """
    read_csv
        Reads CSV content into a list of row dictionaries.

    Parameters:
        filename (str) - path to the file

    Return Value:
        List[Dict[str, str]] - raw CSV content
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def preprocess_data(raw_groups: List[Dict], raw_rooms: List[Dict]) -> tuple[list[Group], list[Room]]:
    """
    preprocess_data
        Converts and validates raw dictionaries into Group and Room objects.

    Parameters:
        raw_groups (List[Dict]) - Raw dicts from CSV
        raw_rooms (List[Dict]) - Raw dicts from CSV

    Return Value:
        tuple[list[Group], list[Room]] - validated and sorted objects

    Exceptions:
        ValueError - if any validation fails
    """
    groups = [parse_group(row, i) for i, row in enumerate(raw_groups)]
    rooms = [parse_room(row, i) for i, row in enumerate(raw_rooms)]

    groups = sorted(groups, key=lambda g: (g.start, -g.size))
    rooms = sorted(rooms, key=lambda r: r.capacity)
    return groups, rooms

def parse_group(row: Dict[str, str], index: int) -> Group:
    """
    parse_group
        Validates and converts a single group entry.

    Parameters:
        row (dict) - raw row from CSV
        index (int) - row index for error context

    Return Value:
        Group - valid structured object

    Exceptions:
        ValueError - If any field fails validation
    """
    try:
        return Group(
            _group_id=row["GroupID"],
            _start=parse_time(row["Start"], "Start"),
            _end=parse_time(row["End"], "End"),
            _size=parse_int(row["Size"], "Size", 1),
            _wheelchair_access=parse_bool(row["WheelchairAccess"], "WheelchairAccess"),
            _projector=parse_bool(row["Projector"], "Projector"),
            _computer=parse_bool(row["Computer"], "Computer"),
            _floor_preference=parse_int(row["FloorPreference"], "FloorPreference", -1)
        )
    except Exception as e:
        group_id = row.get("GroupID", f"(line {index + 2})")
        raise ValueError(f"Invalid group entry {group_id}: {e}")

def parse_room(row: Dict[str, str], index: int) -> Room:
    """
    parse_room
        Validates and converts a single room entry.

    Parameters:
        row (dict) - raw row from CSV
        index (int) - row index for error context

    Return Value:
        Room - valid structured object

    Exceptions:
        ValueError - If any field fails validation
    """
    try:
        return Room(
            _room_id=row["RoomID"],
            _capacity=parse_int(row["Capacity"], "Capacity", 1),
            _wheelchair_access=parse_bool(row["WheelchairAccess"], "WheelchairAccess"),
            _projector=parse_bool(row["Projector"], "Projector"),
            _computer=parse_bool(row["Computer"], "Computer"),
            _floor_level=parse_int(row["FloorLevel"], "FloorLevel", 0)
        )
    except Exception as e:
        room_id = row.get("RoomID", f"(line {index + 2})")
        raise ValueError(f"Invalid room entry {room_id}: {e}")