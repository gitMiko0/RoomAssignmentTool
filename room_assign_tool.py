import sys
from input_reader import read_csv, load_input_data
from solver import backtrack
from output_writer import write_output

# To use this tool, input python room_assign_tool.py <dir of input.csv> <dir of output.csv> in the terminal (while in the project directory)
def main():
    rooms, groups = load_input_data()
    
    assignments = backtrack(groups, rooms, {})
    
    if assignments:
        # Print to terminal
        print("\nAssignments:")
        write_output(filename=None, assignments=assignments)
        write_output("assignments.csv", assignments)
        print("Assignments saved to assignments.csv")
    else:
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()