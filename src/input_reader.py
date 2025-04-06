"""
Module Name: input_reader.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Handles command-line interface and CSV file loading. Reads and validates
input data including room and group information along with the optional time gap setting.
"""

import csv
import sys
from typing import List, Dict, Optional
from .group import Group
from .room import Room
DEFAULT_TIME_GAP = 10  # in minutes

def load_input_data():
    """
    load_input_data
        Reads from sys.argv and loads room and group CSV files,
        along with an optional time gap (in minutes). Exits on error.

    Parameters:
        None

    Return Value:
        tuple - (rooms, groups, time_gap)

    Exceptions:
        SystemExit - If incorrect arguments are passed or file read fails
    """
    try:
        return load_input_data_from_args(sys.argv[1:])
    except ValueError as e:
        print("Error:", e)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        sys.exit(1)

def load_input_data_from_args(args):
    """
    load_input_data_from_args
        Loads data using a custom list of CLI-style arguments.

    Parameters:
        args (list of str) - [rooms_file.csv, groups_file.csv, optional time_gap]

    Return Value:
        tuple - (rooms, groups, time_gap)

    Exceptions:
        ValueError - For invalid or missing arguments
        FileNotFoundError - If files are missing
    """
    if len(args) < 2:
        raise ValueError("Usage: <rooms_file.csv> <groups_file.csv> [time_gap_minutes]")

    rooms_file = args[0]
    groups_file = args[1]
    time_gap = DEFAULT_TIME_GAP

    if len(args) >= 3:
        try:
            time_gap = int(args[2])
        except ValueError:
            raise ValueError("time_gap must be an integer (minutes).")

    rooms = read_csv(rooms_file)
    groups = read_csv(groups_file)
    return rooms, groups, time_gap

def read_csv(filename):
    """
    read_csv
        Reads a CSV file and converts its content into a list of dictionaries.

    Parameters:
        filename (str) - The path to the CSV file to read.

    Return Value:
        list of dict - Each dictionary represents a row in the CSV file.

    Exceptions:
        FileNotFoundError - If the file does not exist.
        Exception - If CSV parsing fails.
    """
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
    
def preprocess_data(raw_groups: List[Dict], raw_rooms: List[Dict]) -> tuple[list[Group], list[Room]]:
    """
    preprocess_data
        Converts input dictionaries into structured Group and Room objects. 
        Also sorts them to improve backtracking efficiency.

    Parameters:
        raw_groups (List[Dict]) - List of raw group dictionaries from CSV or manual entry
        raw_rooms (List[Dict]) - List of raw room dictionaries from CSV or manual entry

    Return Values:
        tuple[list[Group], list[Room]] - Sorted list of Group objects and Room objects
    """
    groups = sorted([Group.from_dict(g) for g in raw_groups], key=lambda g: (g.start, -g.size))
    rooms = sorted([Room.from_dict(r) for r in raw_rooms], key=lambda r: r.capacity)
    return groups, rooms
