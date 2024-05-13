from __init__ import CURSOR, CONN
from employee import Employee  # Update if necessary


class Department:

    all = {}  # Dictionary to store Department instances

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Department instances."""
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT)
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            print(f"Error creating Department table: {e}")

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Department instances."""
        try:
            sql = """
                DROP TABLE IF EXISTS departments
            """
            CURSOR.execute(sql)
            CONN.commit()
        except Exception as e:
            print(f"Error dropping Department table: {e}")

    def save(self):
        """Insert a new row with the name and location values of the current Department instance."""
        try:
            sql = """
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        except Exception as e:
            print(f"Error saving Department instance: {e}")

    # Implement other methods (create, update, delete, instance_from_db, get_all, find_by_id, find_by_name, employees) here...

