import csv

def read_csv(filename):
    """Reads a CSV file and returns the data as a list of dictionaries."""
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)