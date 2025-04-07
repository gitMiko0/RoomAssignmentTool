"""
Module Name: room_assign_tool.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Entry point for CLI execution. Handles top-level orchestration of reading input, solving, and output.

ID Block
Group Member(s): Miko Bengo
Course: COMP 3649 - Programming Paradigms
Instructor: Marc Schroeder
"""

from src.input_reader import load_and_prepare_input
from src.solver import assign_groups
from src.output_writer import write_output

def main():
    groups, rooms, time_gap = load_and_prepare_input()
    result = assign_groups(groups, rooms, time_gap)

    if result:
        write_output(None, result)              # to terminal
        write_output("assignments.csv", result) # to file
    else:
        print("Error: Constraints cannot be satisfied with the provided input.")

if __name__ == "__main__":
    main()
