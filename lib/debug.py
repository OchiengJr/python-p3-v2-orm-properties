#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from department import Department
from employee import Employee
import ipdb  # Remove if not needed


def reset_database():
    """
    Reset the database by dropping existing tables and recreating them,
    and then seeding with initial data.
    """
    try:
        # Drop existing tables
        Employee.drop_table()
        Department.drop_table()
        
        # Create new tables
        Department.create_table()
        Employee.create_table()

        # Seed data
        payroll = Department.create("Payroll", "Building A, 5th Floor")
        human_resources = Department.create(
            "Human Resources", "Building C, East Wing")
        Employee.create("Amir", "Accountant", payroll.id)
        Employee.create("Bola", "Manager", payroll.id)
        Employee.create("Charlie", "Manager", human_resources.id)
        Employee.create("Dani", "Benefits Coordinator", human_resources.id)
        Employee.create("Hao", "New Hires Coordinator", human_resources.id)

        print("Database reset successfully.")

    except Exception as e:
        print(f"Error resetting database: {e}")


# Reset the database and start debugging (remove if not needed)
reset_database()
ipdb.set_trace()
