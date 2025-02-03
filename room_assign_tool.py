import sys
from input_reader import read_csv
from solver import backtrack
from output_writer import write_output

def main():
    rooms_file = sys.argv[1]
    groups_file = sys.argv[2]
    
    rooms = read_csv(rooms_file)
    groups = read_csv(groups_file)
    
    assignments = backtrack(groups, rooms, [])
    
    if assignments:
        write_output("assignments.csv", assignments)
        print("Assignments saved to assignments.csv")
    else:
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()