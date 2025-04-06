import csv

def write_output(filename=None, assignments=None):
    output = []
    for room in assignments:
        for start, end, group in room.schedule:
            output.append({
                'GroupID': group.id,
                'RoomID': room.id,
                'Start': start,
                'End': end
            })

    if filename:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['GroupID', 'RoomID', 'Start', 'End'])
            writer.writeheader()
            writer.writerows(output)
        print(f"\nAssignments written to '{filename}'")
    else:
        print("\nAssignments:")
        for assignment in output:
            print(f"{assignment['GroupID']} --> {assignment['RoomID']} : {assignment['Start']} - {assignment['End']}")
