from __init__ import CURSOR, CONN
from department import Department  # Update if necessary


class Employee:

    all = {}  # Dictionary to store Employee instances

    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    def __repr__(self):
        return (
            f"<Employee {self.id}: {self.name}, {self.job_title}, " +
            f"Department ID: {self.department_id}>"
        )

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Employee instances."""
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                job_title TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id))
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            print(f"Error creating Employee table: {e}")

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Employee instances."""
        try:
            sql = """
                DROP TABLE IF EXISTS employees
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            print(f"Error dropping Employee table: {e}")

    def save(self):
        """Insert a new row with the name, job title, and department id values of the current Employee object."""
        try:
            sql = """
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
            """
            CURSOR.execute(sql, (self.name, self.job_title, self.department_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except Exception as e:
            print(f"Error saving Employee instance: {e}")

    # Implement other methods (update, delete, create, instance_from_db, get_all, find_by_id, find_by_name) here...

