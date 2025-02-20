import csv
from datetime import datetime

# Change this to the actual date you want to append
DEFAULT_DATE = "2025-02-07"

def update_csv(input_file, output_file):
    with open(input_file, mode="r", newline="") as infile, open(output_file, mode="w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Ensure new file has the same structure
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Convert 'Start' and 'End' to include a full date
            row["Start"] = f"{DEFAULT_DATE} {row['Start']}"
            row["End"] = f"{DEFAULT_DATE} {row['End']}"
            writer.writerow(row)

    print(f"Updated CSV saved as {output_file}")

import os
input_path = os.path.join("input", "groups_50.csv")
output_path = os.path.join("input", "groups_50_updated.csv")
update_csv(input_path, output_path)

