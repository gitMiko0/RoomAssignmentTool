import csv, sys

def load_input_data():
    """
    Load input data from command line arguments and CSV files.
    
    Returns:
    tuple: A tuple containing two lists of dictionaries (rooms, groups).
    """
    if len(sys.argv) != 3:
        print("Usage: python room_assign_tool.py <rooms_file.csv> <groups_file.csv>")
        sys.exit(1)
    
    rooms_file = sys.argv[1]
    groups_file = sys.argv[2]
    
    try:
        rooms = read_csv(rooms_file)
        groups = read_csv(groups_file)
        return rooms, groups
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