from .input_reader import load_input_data
from .solver import assign_groups, preprocess_data
from .output_writer import write_output

def main():
    rooms_raw, groups_raw, time_gap = load_input_data()
    groups, rooms = preprocess_data(groups_raw, rooms_raw)
    assignments = assign_groups(groups, rooms, time_gap)

    if assignments:
        write_output(filename=None, assignments=assignments) # Print to console
        write_output("assignments.csv", assignments) # Save to file
    else:
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()
