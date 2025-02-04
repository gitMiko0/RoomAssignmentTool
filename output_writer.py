import csv

def write_output(filename=None, assignments=[]):
    """Writes the room assignment results to a CSV file or prints to the terminal."""
    if filename:
        with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['GroupID', 'RoomID', 'Start', 'End']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(assignments)
    else:
        for assignment in assignments:
            print(f"{assignment['GroupID']} --> {assignment['RoomID']} : {assignment['Start']} - {assignment['End']}")
