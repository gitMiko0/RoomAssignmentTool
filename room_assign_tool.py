import sys
from input_reader import read_csv, load_input_data
from solver import backtrack
from output_writer import write_output

# To use this tool, input python room_assign_tool.py <dir of input.csv> <dir of output.csv> in the terminal (while in the project directory)
def main():
    rooms, groups = load_input_data()
    assignments = backtrack(groups, rooms, {})
    
    if assignments:     # Solution found
        print("\nAssignments:")
        write_output(filename=None, assignments=assignments)    # Print to terminal
        write_output("assignments.csv", assignments)            # Save to file
        print("Assignments saved to assignments.csv")
    else:               # No solution for given input
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()