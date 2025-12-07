"""
Database Schema Generator for SQL Practice Platform

This module creates multiple related tables for practicing various SQL concepts
including JOINs, aggregations, subqueries, and window functions.
"""

import sqlite3
import random
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class Employee:
    """Employee record."""
    employee_id: int
    first_name: str
    last_name: str
    email: str
    department_id: int
    manager_id: Optional[int]
    hire_date: str
    salary: float


class SchemaGenerator:
    """
    Generate comprehensive database schema with multiple related tables.
    """
    
    def __init__(self, db_path: Path, seed: int = 42):
        """
        Initialize schema generator.
        
        Args:
            db_path: Path to SQLite database file
            seed: Random seed for reproducibility
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        random.seed(seed)
        
        # Sample data
        self.first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily',
            'Robert', 'Lisa', 'William', 'Jennifer', 'James', 'Mary',
            'Christopher', 'Patricia', 'Daniel', 'Linda', 'Matthew', 'Barbara'
        ]
        
        self.last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
            'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson'
        ]
        
        self.departments = [
            'Engineering', 'Sales', 'Marketing', 'HR', 'Finance',
            'Operations', 'IT', 'Customer Service'
        ]
        
        self.project_names = [
            'Website Redesign', 'Mobile App', 'Database Migration',
            'Marketing Campaign Q1', 'Sales Automation', 'Cloud Migration',
            'Security Audit', 'Performance Optimization', 'Customer Portal',
            'Analytics Dashboard'
        ]
        
        self.locations = [
            'New York', 'San Francisco', 'Chicago', 'Boston', 'Austin',
            'Seattle', 'Denver', 'Atlanta'
        ]
    
    def create_schema(self) -> None:
        """Create all database tables with proper relationships."""
        
        # Drop existing tables
        self.cursor.execute("DROP TABLE IF EXISTS employee_projects")
        self.cursor.execute("DROP TABLE IF EXISTS projects")
        self.cursor.execute("DROP TABLE IF EXISTS employees")
        self.cursor.execute("DROP TABLE IF EXISTS departments")
        
        # Create departments table
        self.cursor.execute("""
            CREATE TABLE departments (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT NOT NULL,
                location TEXT,
                budget REAL
            )
        """)
        
        # Create employees table
        self.cursor.execute("""
            CREATE TABLE employees (
                employee_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                department_id INTEGER,
                manager_id INTEGER,
                hire_date DATE,
                salary REAL,
                FOREIGN KEY (department_id) REFERENCES departments(department_id),
                FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
            )
        """)
        
        # Create projects table
        self.cursor.execute("""
            CREATE TABLE projects (
                project_id INTEGER PRIMARY KEY,
                project_name TEXT NOT NULL,
                start_date DATE,
                end_date DATE,
                department_id INTEGER,
                budget REAL,
                status TEXT,
                FOREIGN KEY (department_id) REFERENCES departments(department_id)
            )
        """)
        
        # Create employee_projects junction table (many-to-many)
        self.cursor.execute("""
            CREATE TABLE employee_projects (
                employee_id INTEGER,
                project_id INTEGER,
                role TEXT,
                hours_allocated INTEGER,
                PRIMARY KEY (employee_id, project_id),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
        """)
        
        self.conn.commit()
        print("✓ Database schema created successfully")
    
    def populate_departments(self, count: int = 8) -> None:
        """
        Populate departments table.
        
        Args:
            count: Number of departments to create
        """
        departments_data = []
        for i, dept_name in enumerate(self.departments[:count], 1):
            departments_data.append((
                i,
                dept_name,
                random.choice(self.locations),
                random.randint(100000, 1000000)  # Budget
            ))
        
        self.cursor.executemany(
            "INSERT INTO departments VALUES (?, ?, ?, ?)",
            departments_data
        )
        self.conn.commit()
        print(f"✓ Inserted {count} departments")
    
    def populate_employees(self, count: int = 50) -> None:
        """
        Populate employees table with hierarchical relationships.
        
        Args:
            count: Number of employees to create
        """
        employees_data = []
        base_date = datetime(2015, 1, 1)
        
        # Get department IDs
        self.cursor.execute("SELECT department_id FROM departments")
        dept_ids = [row[0] for row in self.cursor.fetchall()]
        
        for i in range(1, count + 1):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            # Use employee ID to ensure unique emails
            email = f"{first_name.lower()}.{last_name.lower()}{i}@company.com"
            
            # First few employees have no manager (executives)
            manager_id = None if i <= 5 else random.randint(1, min(i - 1, 10))
            
            hire_date = (base_date + timedelta(days=random.randint(0, 3000))).strftime('%Y-%m-%d')
            salary = random.randint(40000, 150000)
            
            employees_data.append((
                i,
                first_name,
                last_name,
                email,
                random.choice(dept_ids),
                manager_id,
                hire_date,
                salary
            ))
        
        self.cursor.executemany(
            "INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            employees_data
        )
        self.conn.commit()
        print(f"✓ Inserted {count} employees")
    
    def populate_projects(self, count: int = 15) -> None:
        """
        Populate projects table.
        
        Args:
            count: Number of projects to create
        """
        projects_data = []
        base_date = datetime(2020, 1, 1)
        statuses = ['Active', 'Completed', 'On Hold', 'Cancelled']
        
        # Get department IDs
        self.cursor.execute("SELECT department_id FROM departments")
        dept_ids = [row[0] for row in self.cursor.fetchall()]
        
        for i, project_name in enumerate(self.project_names[:count], 1):
            start_date = (base_date + timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d')
            
            # End date is 30-365 days after start
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = (start_dt + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            
            projects_data.append((
                i,
                project_name,
                start_date,
                end_date,
                random.choice(dept_ids),
                random.randint(50000, 500000),  # Budget
                random.choice(statuses)
            ))
        
        self.cursor.executemany(
            "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?)",
            projects_data
        )
        self.conn.commit()
        print(f"✓ Inserted {count} projects")
    
    def populate_employee_projects(self) -> None:
        """
        Populate employee_projects junction table.
        Creates many-to-many relationships between employees and projects.
        """
        # Get all employee and project IDs
        self.cursor.execute("SELECT employee_id FROM employees")
        employee_ids = [row[0] for row in self.cursor.fetchall()]
        
        self.cursor.execute("SELECT project_id FROM projects")
        project_ids = [row[0] for row in self.cursor.fetchall()]
        
        roles = ['Lead', 'Developer', 'Analyst', 'Designer', 'QA', 'Support']
        employee_project_data = []
        
        # Assign 2-5 employees to each project
        for project_id in project_ids:
            num_employees = random.randint(2, 5)
            assigned_employees = random.sample(employee_ids, num_employees)
            
            for emp_id in assigned_employees:
                employee_project_data.append((
                    emp_id,
                    project_id,
                    random.choice(roles),
                    random.randint(10, 40)  # Hours per week
                ))
        
        self.cursor.executemany(
            "INSERT INTO employee_projects VALUES (?, ?, ?, ?)",
            employee_project_data
        )
        self.conn.commit()
        print(f"✓ Inserted {len(employee_project_data)} employee-project assignments")
    
    def generate_all(
        self,
        num_departments: int = 8,
        num_employees: int = 50,
        num_projects: int = 15
    ) -> None:
        """
        Generate complete database with all tables populated.
        
        Args:
            num_departments: Number of departments
            num_employees: Number of employees
            num_projects: Number of projects
        """
        print("\nGenerating enhanced database schema...")
        print("=" * 60)
        
        self.create_schema()
        self.populate_departments(num_departments)
        self.populate_employees(num_employees)
        self.populate_projects(num_projects)
        self.populate_employee_projects()
        
        print("=" * 60)
        print("✓ Database generation complete!\n")
        
        # Display summary
        self.display_summary()
    
    def display_summary(self) -> None:
        """Display summary of generated data."""
        tables = ['departments', 'employees', 'projects', 'employee_projects']
        
        print("Database Summary:")
        print("-" * 40)
        
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"  {table:25} {count:5} rows")
        
        print("-" * 40)
    
    def close(self) -> None:
        """Close database connection."""
        self.conn.close()


def main():
    """Main execution function."""
    # Use output directory
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = output_dir / 'generated_data.db'
    
    # Generate schema
    generator = SchemaGenerator(db_path)
    generator.generate_all(
        num_departments=8,
        num_employees=50,
        num_projects=15
    )
    generator.close()
    
    print(f"\n✓ Database saved to: {db_path}")
    print("\nExample queries you can now practice:")
    print("  • SELECT * FROM employees;")
    print("  • SELECT * FROM departments;")
    print("  • SELECT e.*, d.department_name FROM employees e JOIN departments d ON e.department_id = d.department_id;")
    print("  • SELECT department_id, AVG(salary) FROM employees GROUP BY department_id;")


if __name__ == "__main__":
    main()
