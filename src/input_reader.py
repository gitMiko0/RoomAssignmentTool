"""
Module Name: input_loader.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Handles command-line interface and CSV file loading. Reads and validates
input data including room and group information along with the optional time gap setting.
"""

import csv
import sys

DEFAULT_TIME_GAP = 10  # in minutes

def load_input_data():
    """
    load_input_data
        Reads command-line arguments to load room and group CSV files,
        along with an optional time gap (in minutes).

    Parameters:
        None (reads from sys.argv)

    Return Value:
        tuple - (rooms, groups, time_gap)
            rooms (list of dict) - Raw CSV data for room entries
            groups (list of dict) - Raw CSV data for group entries
            time_gap (int) - Optional time buffer in minutes between bookings

    Exceptions:
        SystemExit - If incorrect arguments are passed or file read fails
    """
    if len(sys.argv) < 3:
        print("Usage: python room_assign_tool.py <rooms_file.csv> <groups_file.csv> [time_gap_minutes]")
        sys.exit(1)

    rooms_file = sys.argv[1]
    groups_file = sys.argv[2]
    time_gap = DEFAULT_TIME_GAP

    if len(sys.argv) >= 4:
        try:
            time_gap = int(sys.argv[3])
        except ValueError:
            print("Error: time_gap must be an integer (minutes).")
            sys.exit(1)

    try:
        rooms = read_csv(rooms_file)
        groups = read_csv(groups_file)
        return rooms, groups, time_gap
    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        sys.exit(1)

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
