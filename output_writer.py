import csv

def write_output(filename, assignments):
    """Writes the room assignment results to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['GroupID', 'RoomID', 'Start', 'End']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(assignments)