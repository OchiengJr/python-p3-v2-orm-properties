from department import Department
from employee import Employee
import pytest


class TestEmployeeProperties:
    '''Test cases for the properties of the Employee class.'''

    @pytest.fixture(autouse=True)
    def reset_db(self):
        '''Fixture to drop and recreate tables prior to each test.'''
        Employee.drop_table()
        Department.drop_table()
        Employee.create_table()
        Department.create_table()
        # Clear the object cache
        Department.all = {}
        Employee.all = {}

    def test_name_job_department_valid(self):
        '''Validates that name, job title, and department id are valid.'''
        # Should not raise an exception
        department = Department.create("Payroll", "Building A, 5th Floor")
        employee = Employee.create("Lee", "Manager", department.id)

    def test_name_is_string(self):
        '''Validates that the name property is assigned a string.'''
        with pytest.raises(ValueError):
            department = Department.create("Payroll", "Building A, 5th Floor")
            employee = Employee.create("Lee", "Manager", department.id)
            employee.name = 7

    def test_name_string_length(self):
        '''Validates that the name property length is greater than 0.'''
        with pytest.raises(ValueError):
            department = Department.create("Payroll", "Building A, 5th Floor")
            employee = Employee.create("Lee", "Manager", department.id)
            employee.name = ''

    def test_job_title_is_string(self):
        '''Validates that the job title property is assigned a string.'''
        with pytest.raises(ValueError):
            department = Department.create("Payroll", "Building A, 5th Floor")
            employee = Employee.create("Lee", "Manager", department.id)
            employee.job_title = 7

    def test_job_title_string_length(self):
        '''Validates that the job title property length is greater than 0.'''
        with pytest.raises(ValueError):
            department = Department.create("Payroll", "Building A, 5th Floor")
            employee = Employee.create("Lee", "Manager", department.id)
            employee.job_title = ''

    def test_department_property(self):
        '''Validates that the department property is assigned a valid Department instance.'''
        department = Department.create("Payroll", "Building C, 3rd Floor")
        employee = Employee.create("Raha", "Accountant", department.id)  # No exception

    def test_department_property_fk(self):
        '''Validates that the department property is assigned a valid foreign key.'''
        with pytest.raises(ValueError):
            Employee.create("Raha", "Accountant", 7)

    def test_department_property_type(self):
        '''Validates that the department property type is enforced.'''
        with pytest.raises(ValueError):
            employee = Employee.create("Raha", "Accountant", "abc")
