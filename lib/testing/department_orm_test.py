from __init__ import CONN, CURSOR
from department import Department
from employee import Employee
import pytest


class TestDepartment:
    '''Test cases for the Department class.'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''Fixture to drop tables prior to each test.'''
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        Department.all = {}

    def test_creates_table(self):
        '''Test that create_table method creates the "departments" table if it doesn't exist.'''
        Department.create_table()
        cursor = CONN.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='departments'")
        table_exists = cursor.fetchone()
        assert table_exists is not None, "Failed to create the 'departments' table."

    def test_drops_table(self):
        '''Test that drop_table method drops the "departments" table if it exists.'''
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
        Department.drop_table()
        sql_table_names = "SELECT name FROM sqlite_master WHERE type='table' AND name='departments'"
        result = CURSOR.execute(sql_table_names).fetchone()
        assert result is None, "Failed to drop the 'departments' table."

    def test_saves_department(self):
        '''Test that save method saves a Department instance to the db and assigns the instance an id.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        sql = "SELECT * FROM departments"
        row = CURSOR.execute(sql).fetchone()
        assert row == (department.id, department.name, department.location)

    # Add other test cases here...

if __name__ == "__main__":
    pytest.main()
