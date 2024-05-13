from department import Department
import pytest


class TestDepartmentProperties:
    '''Test cases for the properties of the Department class.'''

    @pytest.fixture(autouse=True)
    def clear_dictionary(self):
        '''Fixture to clear out the class dictionary.'''
        Department.all = {}

    def test_name_location_valid(self):
        '''Validates that name and location are assigned valid non-empty strings.'''
        # Should not throw an exception
        department = Department("Payroll", "Building A, 5th Floor")

    def test_name_is_string(self):
        '''Validates that the name property is assigned a string.'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            department.name = 7

    def test_name_string_length(self):
        '''Validates that the name property has a length > 0.'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            department.name = ''

    def test_location_is_string(self):
        '''Validates that the location property is assigned a string.'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            department.location = True

    def test_location_string_length(self):
        '''Validates that the location property has a length > 0.'''
        with pytest.raises(ValueError):
            department = Department("Payroll", "Building A, 5th Floor")
            department.location = ''
