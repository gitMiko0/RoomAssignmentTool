"""
Module Name: output_writer.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Handles formatting and writing the final room assignment results
either to a CSV file or directly to the console.

Module Summary:
- Converts finalized room-group assignments into output-ready dictionaries.
- Writes formatted assignment data to either a CSV file or standard output.

Dependencies:
- csv module for file output
- Room and Group object access patterns

Known/Suspected Errors:
- None known at this time.
"""

import csv

def write_output(filename=None, assignments=None):
    """
    write_output
        Outputs the final group-to-room assignments. If a filename is given, writes to a CSV.
        Otherwise, prints to the console.

    Parameters:
        filename (str, optional) - the path to write the CSV output to; if None, print to console
        assignments (List[Room]) - list of Room objects with group schedules to output

    Output Format:
        GroupID, RoomID, Start, End - either printed or written in CSV header order

    Raises:
        None explicitly, but may throw file I/O errors if path is invalid
    """
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
