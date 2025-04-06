"""
Module Name: test_input_loader.py
Project Name: Room Assignment Tool (Imperative Solution)
File Purpose: Unit tests for parsing and preprocessing CSV input into proper Group and Room objects.
"""

import unittest
from datetime import datetime
from src.input_reader import read_csv, preprocess_data
from src.group import Group
from src.room import Room

class TestInputLoader(unittest.TestCase):

    def setUp(self):
        self.groups_path = "./tests/test_groups.csv"
        self.rooms_path = "./tests/test_rooms.csv"

    def test_preprocess_data_returns_typed_group_objects(self):
        raw_groups = read_csv(self.groups_path)
        raw_rooms = read_csv(self.rooms_path)
        groups, _ = preprocess_data(raw_groups, raw_rooms)

        g1 = groups[0]
        self.assertIsInstance(g1, Group)
        self.assertEqual(g1.id, "G0001")
        self.assertEqual(g1.size, 40)
        self.assertEqual(g1.start, datetime(2025, 2, 7, 8, 0))
        self.assertTrue(g1.projector)
        self.assertFalse(g1.computer)
        self.assertTrue(g1.wheelchair_access)

    def test_preprocess_data_returns_typed_room_objects(self):
        raw_groups = read_csv(self.groups_path)
        raw_rooms = read_csv(self.rooms_path)
        _, rooms = preprocess_data(raw_groups, raw_rooms)

        r1 = rooms[0]
        self.assertIsInstance(r1, Room)
        self.assertEqual(r1.id, "R101")
        self.assertEqual(r1.capacity, 25)
        self.assertEqual(r1.floor_level, 1)

if __name__ == "__main__":
    unittest.main()
