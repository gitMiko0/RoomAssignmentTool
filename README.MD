# Imperative Solution: Room Assignment Tool

This tool assigns groups into pre-existing rooms while checking for multiple constraints such as:

- **Computer and projector availability**
- **Wheelchair accessibility**
- **Room capacity**
- **Floor preference** (-1 to indicate no preference)
- **Time conflicts**, with a user-defined **time gap** (in minutes) between bookings

The tool ensures that no invalid assignments are made. If a solution exists that satisfies all the constraints, it will find it using a backtracking algorithm.
Otherwise, the tool will communicate that it is not able to find a viable solution.

---

## Input Format

The tool expects two **comma-separated value (.csv)** files as input:

1. `rooms.csv` – contains room properties like capacity, equipment, accessibility, and floor level.
2. `groups.csv` – contains group scheduling info, size, required equipment, accessibility, and floor preferences.

Sample fields:
- **Room file:** `RoomID,Capacity,WheelchairAccess,Projector,Computer,FloorLevel`
- **Group file:** `GroupID,Start,End,Size,WheelchairAccess,Projector,Computer,FloorPreference`

3. Optional: time gap (in minutes)


---

## How to run the tool?

From the terminal, run:

```bash
python -m src.room_assign_tool <rooms_file.csv> <groups_file.csv> <time_gap>
```
## How to run the tests?
```bash
python -m coverage run -m pytest test_tool.py
python -m coverage report
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

### How to Get the Executable

If the executable is not built yet, it can be generated it using [PyInstaller](https://pyinstaller.org/en/stable/) (see below).  
