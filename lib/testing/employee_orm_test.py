from __init__ import CONN, CURSOR
from employee import Employee
from department import Department
from faker import Faker
import pytest


class TestEmployee:
    '''Test cases for the Employee class.'''

    @pytest.fixture(autouse=True)
    def drop_tables(self):
        '''Fixture to drop tables prior to each test.'''
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")

        Department.all = {}
        Employee.all = {}

    def test_creates_table(self):
        '''Validates that the create_table() method creates the employees table.'''
        Department.create_table()  # Ensure Department table exists due to FK constraint
        Employee.create_table()
        assert (CURSOR.execute("SELECT * FROM employees"))

    def test_drops_table(self):
        '''Validates that the drop_table() method drops the employees table.'''
        sql = """
            CREATE TABLE IF NOT EXISTS departments
                (id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT)
        """
        CURSOR.execute(sql)

        sql = """  
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id))
        """
        CURSOR.execute(sql)

        Employee.drop_table()

        # Confirm departments table exists
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='departments'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result)

        # Confirm employees table does not exist
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='employees'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        assert (result is None)

    def test_saves_employee(self):
        '''Validates that the save() method saves an Employee instance to the database.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        Employee.create_table()
        employee = Employee("Sasha", "Manager", department.id)
        employee.save()

        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee.id, "Sasha", "Manager", department.id))

    def test_creates_employee(self):
        '''Validates that the create() method creates a new Employee instance and saves it to the database.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        Employee.create_table()
        employee = Employee.create("Kai", "Web Developer", department.id)

        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee.id, "Kai", "Web Developer", department.id))

    def test_updates_row(self):
        '''Validates that the update() method updates an employee's corresponding database record.'''
        Department.create_table()
        department1 = Department("Payroll", "Building A, 5th Floor")
        department1.save()
        department2 = Department("Human Resources", "Building C, 2nd Floor")
        department2.save()

        Employee.create_table()

        employee1 = Employee("Raha", "Accountant", department1.id)
        employee1.save()
        employee2 = Employee("Tal", "Benefits Coordinator", department2.id)
        employee2.save()
        id1 = employee1.id

        employee1.name = "Raha Lee"
        employee1.job_title = "Senior Accountant"
        employee1.department_id = department2.id
        employee1.update()

        # Confirm employee updated
        employee = Employee.find_by_id(id1)
        assert ((employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee1.id, employee1.name, employee1.job_title, employee1.department_id) ==
                (id1, "Raha Lee", "Senior Accountant", department2.id))

        # Confirm employee not updated
        employee = Employee.find_by_id(employee2.id)
        assert ((employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee2.id, employee2.name, employee2.job_title, employee2.department_id))

    def test_deletes_row(self):
        '''Validates that the delete() method deletes the employee's corresponding database record.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        Employee.create_table()

        employee1 = Employee("Raha", "Accountant", department.id)
        employee1.save()
        id1 = employee1.id
        employee2 = Employee("Tal", "Benefits Coordinator", department.id)
        employee2.save()
        id2 = employee2.id

        employee1.delete()
        # Confirm row deleted
        assert (Employee.find_by_id(id1) is None)
        # Confirm Employee object state is correct, id should be None
        assert ((employee1.id, employee1.name, employee1.job_title, employee1.department_id) ==
                (None, "Raha", "Accountant", department.id))
        # Confirm dictionary entry was deleted
        assert (Employee.all.get(id1) is None)

        # Confirm employee2 row not modified, employee2 object not modified
        employee = Employee.find_by_id(id2)
        assert ((employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee2.id, employee2.name, employee2.job_title, employee2.department_id))

    def test_instance_from_db(self):
        '''Validates that the instance_from_db() method creates an Employee instance from a database row.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        Employee.create_table()
        sql = """
            INSERT INTO employees (name, job_title, department_id)
            VALUES ('Amir', 'Programmer', ?)
        """
        CURSOR.execute(sql, (department.id,))
        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()

        employee = Employee.instance_from_db(row)
        assert ((row[0], row[1], row[2], row[3]) ==
                (employee.id, employee.name, employee.job_title, employee.department_id) ==
                (employee.id, "Amir", "Programmer", department.id))

    def test_gets_all(self):
        '''Validates that the get_all() method returns a list of all Employee instances from the database.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()

        Employee.create_table()
        employee1 = Employee("Tristan", "Fullstack Developer", department.id)
        employee1.save()
        employee2 = Employee("Sasha", "Manager", department.id)
        employee2.save()

        employees = Employee.get_all()
        assert (len(employees) == 2)
        assert ((employees[0].id, employees[0].name, employees[0].job_title, employees[0].department_id) ==
                (employee1.id, employee1.name, employee1.job_title, employee1.department_id))
        assert ((employees[1].id, employees[1].name, employees[1].job_title, employees[1].department_id) ==
                (employee2.id, employee2.name, employee2.job_title, employee2.department_id))

    def test_finds_by_name(self):
        '''Validates that the find_by_name() method returns an Employee instance corresponding to the database row retrieved by name.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        faker = Faker()
        employee1 = Employee(faker.name(), "Manager", department.id)
        employee1.save()
        employee2 = Employee(faker.name(), "Web Developer", department.id)
        employee2.save()

        employee = Employee.find_by_name(employee1.name)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee1.id, employee1.name, employee1.job_title, employee1.department_id)
        )

        employee = Employee.find_by_name(employee2.name)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee2.id, employee2.name, employee2.job_title, employee2.department_id)
        )

        employee = Employee.find_by_name("Unknown")
        assert (employee is None)

    def test_finds_by_id(self):
        '''Validates that the find_by_id() method returns an Employee instance corresponding to the database row retrieved by id.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        faker = Faker()
        employee1 = Employee(faker.name(), "Manager", department.id)
        employee1.save()
        employee2 = Employee(faker.name(), "Web Developer", department.id)
        employee2.save()

        employee = Employee.find_by_id(employee1.id)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee1.id, employee1.name, employee1.job_title, employee1.department_id)
        )

        employee = Employee.find_by_id(employee2.id)
        assert (
            (employee.id, employee.name, employee.job_title, employee.department_id) ==
            (employee2.id, employee2.name, employee2.job_title, employee2.department_id)
        )

        employee = Employee.find_by_id(3)
        assert (employee is None)
