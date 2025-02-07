import pytest  # type: ignore
from solver import backtrack, is_valid_assignment

@pytest.fixture
def sample_data_no_groups():
    return {
        'groups': [],
        'rooms': [
            {'RoomID': 'R101', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'},
            {'RoomID': 'R102', 'Capacity': '10', 'Computer': 'FALSE', 'FloorLevel': '2', 'Projector': 'FALSE', 'WheelchairAccess': 'FALSE'}
        ]
    }

@pytest.fixture
def sample_data_wheelchair_access():
    return {
        'groups': [
            {'GroupID': 'G1', 'Size': '10', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'TRUE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '-1'},
            {'GroupID': 'G2', 'Size': '5', 'Start': '10:30', 'End': '11:30', 'WheelchairAccess': 'FALSE', 'Projector': 'TRUE', 'Computer': 'TRUE', 'FloorPreference': '-1'}
        ],
        'rooms': [
            {'RoomID': 'R101', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'},
            {'RoomID': 'R102', 'Capacity': '10', 'Computer': 'FALSE', 'FloorLevel': '2', 'Projector': 'FALSE', 'WheelchairAccess': 'FALSE'}
        ]
    }

@pytest.fixture
def sample_data_capacity_check():
    return {
        'groups': [{'GroupID': 'G1', 'Size': '20', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'TRUE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '-1'}],
        'rooms': [{'RoomID': 'R101', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'}]
    }

@pytest.fixture
def sample_data_floor_preference():
    return {
        'groups': [{'GroupID': 'G1', 'Size': '10', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'TRUE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '2'}],
        'rooms': [
            {'RoomID': 'R101', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'},
            {'RoomID': 'R102', 'Capacity': '10', 'Computer': 'TRUE', 'FloorLevel': '2', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'}
        ]
    }

@pytest.fixture
def sample_data_no_rooms():
    return {
        'groups': [
            {'GroupID': 'G1', 'Size': '10', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'TRUE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '-1'}
        ],
        'rooms': []
    }

@pytest.fixture
def sample_data_room_capacity_check():
    return {
        'groups': [
            {'GroupID': 'G1', 'Size': '30', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'TRUE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '-1'}
        ],
        'rooms': [
            {'RoomID': 'R101', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'}
        ]
    }

@pytest.fixture
def sample_data_floor_preference_check():
    return {
        'groups': [
            {'GroupID': 'G1', 'Size': '15', 'Start': '09:00', 'End': '10:00', 'WheelchairAccess': 'FALSE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '2'}
        ],
        'rooms': [
            {'RoomID': 'R102', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '1', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'},
            {'RoomID': 'R102', 'Capacity': '15', 'Computer': 'TRUE', 'FloorLevel': '2', 'Projector': 'TRUE', 'WheelchairAccess': 'TRUE'}
        ]
    }

def test_no_groups(sample_data_no_groups):
    assignments = backtrack(sample_data_no_groups['groups'], sample_data_no_groups['rooms'])
    assert assignments == [], "There should be no assignments when there are no groups."

def test_wheelchair_access(sample_data_wheelchair_access):
    assignments = backtrack(sample_data_wheelchair_access['groups'], sample_data_wheelchair_access['rooms'])
    assert len(assignments) == 2, "Both groups should be assigned to rooms."
    assert assignments[0]['RoomID'] == 'R101', "Group G1 should be assigned to a room with wheelchair access (R101)."
    assert assignments[1]['RoomID'] == 'R101', "Group G1 should be assigned to R101 which is now free."

def test_capacity_check(sample_data_capacity_check):
    assignments = backtrack(sample_data_capacity_check['groups'], sample_data_capacity_check['rooms'])
    assert assignments == [], "Group G1 should not be assigned to R101 due to capacity issue."

def test_no_rooms(sample_data_no_rooms):
    assignments = backtrack(sample_data_no_rooms['groups'], sample_data_no_rooms['rooms'])
    assert assignments == [], "There should be no assignments when there are no rooms."

def test_room_capacity_check(sample_data_room_capacity_check):
    assignments = backtrack(sample_data_room_capacity_check['groups'], sample_data_room_capacity_check['rooms'])
    assert assignments == [], "Group G1 should not be assigned to R101 due to capacity issue."


def test_no_possible_assignment():
    impossible_data = {
        'groups': [
            {'GroupID': 'G1', 'Start': '09:00', 'End': '10:00', 'Size': '30', 'Projector': 'TRUE', 'Computer': 'TRUE', 'WheelchairAccess': 'TRUE', 'FloorPreference': '1'},
            {'GroupID': 'G2', 'Start': '10:05', 'End': '11:05', 'Size': '25', 'Projector': 'TRUE', 'Computer': 'TRUE', 'WheelchairAccess': 'TRUE', 'FloorPreference': '1'}
        ],
        'rooms': [
            {'RoomID': 'R101', 'Capacity': '20', 'Projector': 'TRUE', 'Computer': 'TRUE', 'WheelchairAccess': 'TRUE', 'FloorLevel': '1'}
        ]
    }

    # Run the backtracking algorithm
    result = backtrack(impossible_data['groups'], impossible_data['rooms'])

    # Since no assignment is possible, the result should be an empty list
    assert result == [], "Expected an empty assignment list when no valid solution exists."

def test_floor_preference_check(sample_data_floor_preference_check):
    assignments = backtrack(sample_data_floor_preference_check['groups'], sample_data_floor_preference_check['rooms'])
    assert assignments[0]['RoomID'] == 'R101', "Group G1 should be assigned to R101 on floor 1."