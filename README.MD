# Imperative Solution: Room Assignment Tool

This tool assigns groups into pre-existing rooms while checking for multiple constraints such as:

- **Computer and projector availability**    TRUE or FALSE
- **Wheelchair accessibility**               TRUE or FALSE
- **Room capacity**                          TRUE or FALSE
- **Floor preference**                       (-1 to indicate no preference)
- **Time conflicts**, with a user-defined **time gap** (in minutes) between bookings

The tool ensures that no invalid assignments are made. If a solution exists that satisfies all the constraints, it will find it using a backtracking algorithm.
Otherwise, the tool will communicate that it is not able to find a viable solution.

---

## Input Format

The tool expects two **comma-separated value (.csv)** files as input:

1. `rooms.csv` – contains room properties like capacity, equipment, accessibility, and floor level.
2. `groups.csv` – contains group scheduling info, size, required equipment, accessibility, and floor preferences.

The input must have the following headers:
- **Room file:** `RoomID,Capacity,WheelchairAccess,Projector,Computer,FloorLevel`
- **Group file:** `GroupID,Start,End,Size,WheelchairAccess,Projector,Computer,FloorPreference`

Sample inputs are provided in the input folder (consult groups_50.csv and/or rooms_50.csv as valid samples)

**IDs MUST be UNIQUE**
**Date & Time are in the format: YYYY-MM-DD HH:MM**

3. Optional: time gap (in minutes)
In the CLI, the tool can have a third optional input. If this isn't provided it will assume a 10-minutes gap between bookings.


---

## How to run the tool?

From the terminal, run:

```bash
python -m src.room_assign_tool <rooms_file.csv> <groups_file.csv> <time_gap>
```
## How to run the tests?
The test is just an automated powershell script calling the executable and the appropriate files. Run this with:
```bash
./black_box_tests.ps1
```

---

## Running the Executable

This tool is also available as a standalone executable — no need to install Python or any dependencies.
Please find the executable in /dist/room_assign_tool.exe

### Running the Executable
Once you have the executable (`room_assign_tool.exe`), run it similarly via Command Prompt:

```bash
room_assign_tool.exe <rooms_file.csv> <groups_file.csv> --gap <minutes> [--output output_file.csv]
```
Ensure that you are on the directory where the executable is located!

Note: The testing also has comprehensive, implementation-based, function specific tests with pytest along with coverage reports under the tests folder. Please ignore this.

### How to Get the Executable

If desired, it can be generated it using [PyInstaller](https://pyinstaller.org/en/stable/). 
