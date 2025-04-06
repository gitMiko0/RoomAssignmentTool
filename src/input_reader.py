import csv
import sys

DEFAULT_TIME_GAP = 10  # in minutes

def load_input_data():
    """
    Load input data from command line arguments and CSV files.
    
    Returns:
    tuple: (rooms, groups, time_gap)
    - rooms: List of room dictionaries
    - groups: List of group dictionaries
    - time_gap: Integer time buffer in minutes
    """
    if len(sys.argv) < 3:
        print("Usage: python room_assign_tool.py <rooms_file.csv> <groups_file.csv> [time_gap_minutes]")
        sys.exit(1)

    rooms_file = sys.argv[1]
    groups_file = sys.argv[2]
    time_gap = DEFAULT_TIME_GAP

    # Optional: time gap as 3rd argument
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
    """Reads a CSV file and returns the data as a list of dictionaries."""
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
