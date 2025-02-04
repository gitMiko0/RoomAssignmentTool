import sys
from input_reader import read_csv
from solver import backtrack
from output_writer import write_output

# To use this tool, input python room_assign_tool.py <dir of input.csv> <dir of output.csv> in the terminal (while in the project directory)
def main():
    rooms_file = sys.argv[1]
    groups_file = sys.argv[2]
    
    rooms = read_csv(rooms_file)    # This data structure is a list of dictionaries
    groups = read_csv(groups_file)
    
    assignments = backtrack(groups, rooms, []) # Holds existing paths being explored (comprehended as a non-deterministic tree)
    
    if assignments:
        write_output(assignments=assignments)
        write_output("assignments.csv", assignments)
        print("Assignments saved to assignments.csv")
    else:
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()