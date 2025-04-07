"""
Module Name: validators.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose:
    Contains reusable validation and conversion functions for parsing and validating CSV field data.

Module Summary:
    This module provides helper functions to verify and convert input values from strings into 
    strongly-typed formats. It enforces strict formatting and ensures that values meet expected 
    constraints such as boolean correctness, datetime formatting, and numeric range bounds.

Key Functions:
    - parse_bool
    - parse_int
    - parse_time

Dependencies:
    - datetime (for parsing timestamps)

Known/Suspected Errors:
    - None currently known
"""

from datetime import datetime

def parse_bool(val: str, field: str) -> bool:
    """
    parse_bool
        Converts a string value into a boolean if it matches 'TRUE' or 'FALSE' (case-insensitive).

    Parameters:
        val (str) - The raw string value from input.
        field (str) - The name of the field being parsed (used for error messages).

    Return Value:
        bool - True if val is 'TRUE', False if 'FALSE'.

    Exceptions:
        ValueError - If the value is not 'TRUE' or 'FALSE' (case-insensitive).
    """
    val_upper = val.strip().upper()
    if val_upper not in ("TRUE", "FALSE"):
        raise ValueError(f"Invalid boolean value '{val}' in field '{field}' (expected TRUE or FALSE)")
    return val_upper == "TRUE"

def parse_int(val: str, field: str, min_allowed: int = None) -> int:
    """
    parse_int
        Converts a string to an integer, and optionally checks that it's above a minimum threshold.

    Parameters:
        val (str) - The raw string value from input.
        field (str) - The name of the field being parsed.
        min_allowed (int) - An optional minimum value to enforce (inclusive).

    Return Value:
        int - The parsed integer value.

    Exceptions:
        ValueError - If the value is not a valid integer or doesn't meet the minimum requirement.
    """
    try:
        i = int(val.strip())
        if min_allowed is not None and i < min_allowed:
            raise ValueError(f"{field} must be >= {min_allowed}, got {i}")
        return i
    except ValueError:
        raise ValueError(f"Invalid integer '{val}' in field '{field}' Expected integer <= {min_allowed}")

def parse_time(val: str, field: str) -> datetime:
    """
    parse_time
        Parses a string in the format 'YYYY-MM-DD HH:MM' into a datetime object.

    Parameters:
        val (str) - The timestamp string to parse.
        field (str) - The name of the field being parsed (used for error messages).

    Return Value:
        datetime - The parsed datetime object.

    Exceptions:
        ValueError - If the input string does not match the expected timestamp format.
    """
    try:
        return datetime.strptime(val.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(f"Invalid datetime '{val}' in field '{field}' (expected format YYYY-MM-DD HH:MM)")
