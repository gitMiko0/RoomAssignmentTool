import pytest
from solver import is_valid_assignment

@pytest.fixture
def sample_data():
    return {
        'group': {'GroupID': 'G1', 'Size': '10', 'Start': '10:00', 'End': '11:00',
                  'WheelchairAccess': 'FALSE', 'Projector': 'FALSE', 'Computer': 'FALSE', 'FloorPreference': '-1'},
        'room': {'RoomID': 'R101', 'Capacity': '15', 'WheelchairAccess': 'TRUE',
                 'Projector': 'TRUE', 'Computer': 'TRUE', 'FloorLevel': '1'},
        'assignments': []
    }

def test_valid_assignment(sample_data):
    assert is_valid_assignment(sample_data['group'], sample_data['room'], sample_data['assignments']) == True

def test_capacity_constraint(sample_data):
    sample_data['group']['Size'] = '20'  # Exceeds capacity
    assert is_valid_assignment(sample_data['group'], sample_data['room'], sample_data['assignments']) == False

def test_time_gap_violation(sample_data):
    sample_data['assignments'].append({'GroupID': 'G2', 'RoomID': 'R101', 'Start': '09:30', 'End': '10:10'})
    assert is_valid_assignment(sample_data['group'], sample_data['room'], sample_data['assignments']) == False
    print("Test: Time Constraint Passed!")
