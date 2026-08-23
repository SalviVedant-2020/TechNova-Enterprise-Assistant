import sqlite3
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker()

DATABASE_PATH = "database/company.db"

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()


# ============================================================
# DROP TABLES
# ============================================================

cursor.executescript("""
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS performance_reviews;
DROP TABLE IF EXISTS leave_requests;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
""")


# ============================================================
# CREATE TABLES
# ============================================================

cursor.execute("""
CREATE TABLE departments(

    department_id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    head_employee_id INTEGER

)
""")


cursor.execute("""
CREATE TABLE employees(

    employee_id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    email TEXT UNIQUE,

    department_id INTEGER,

    job_title TEXT,

    joining_date DATE,

    salary INTEGER,

    manager_id INTEGER,

    FOREIGN KEY(department_id)
        REFERENCES departments(department_id),

    FOREIGN KEY(manager_id)
        REFERENCES employees(employee_id)

)
""")


cursor.execute("""
CREATE TABLE projects(

    project_id INTEGER PRIMARY KEY,

    project_name TEXT,

    department_id INTEGER,

    status TEXT,

    budget INTEGER,

    FOREIGN KEY(department_id)
        REFERENCES departments(department_id)

)
""")


cursor.execute("""
CREATE TABLE employee_projects(

    employee_id INTEGER,

    project_id INTEGER,

    PRIMARY KEY(employee_id, project_id),

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id),

    FOREIGN KEY(project_id)
        REFERENCES projects(project_id)

)
""")


cursor.execute("""
CREATE TABLE leave_requests(

    leave_id INTEGER PRIMARY KEY,

    employee_id INTEGER,

    leave_type TEXT,

    start_date DATE,

    end_date DATE,

    status TEXT,

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

)
""")


cursor.execute("""
CREATE TABLE performance_reviews(

    review_id INTEGER PRIMARY KEY,

    employee_id INTEGER,

    review_year INTEGER,

    rating REAL,

    training_completed BOOLEAN,

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

)
""")


cursor.execute("""
CREATE TABLE attendance(

    attendance_id INTEGER PRIMARY KEY,

    employee_id INTEGER,

    date DATE,

    work_mode TEXT,

    hours_worked REAL,

    FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)

)
""")


# ============================================================
# STATIC COMPANY DATA
# ============================================================

departments = [
    "Engineering",
    "Human Resources",
    "Finance",
    "Marketing",
    "Sales",
    "Operations"
]


job_titles = {

    "Engineering": [
        ("Software Engineer", 900000, 1500000),
        ("Senior Software Engineer", 1500000, 2200000),
        ("Tech Lead", 2200000, 3000000),
    ],

    "Human Resources": [
        ("HR Executive", 500000, 800000),
        ("HR Manager", 1000000, 1800000),
    ],

    "Finance": [
        ("Financial Analyst", 700000, 1200000),
        ("Finance Manager", 1500000, 2200000),
    ],

    "Marketing": [
        ("Marketing Executive", 600000, 1000000),
        ("Marketing Manager", 1200000, 1800000),
    ],

    "Sales": [
        ("Sales Executive", 700000, 1300000),
        ("Sales Manager", 1500000, 2200000),
    ],

    "Operations": [
        ("Operations Executive", 700000, 1200000),
        ("Operations Manager", 1400000, 2000000),
    ]

}


project_names = [

    "Project Atlas",
    "Project Nova",
    "Project Phoenix",
    "AI Knowledge Assistant",
    "Customer 360",
    "Sales Insight",
    "HR Automation",
    "Expense Tracker",
    "Payroll Modernization",
    "Data Warehouse",
    "Marketing Pulse",
    "CRM Upgrade",
    "Inventory Sync",
    "Risk Dashboard",
    "Compliance Portal"

]


leave_types = [
    "Casual Leave",
    "Sick Leave",
    "Earned Leave"
]


leave_status = [
    "Approved",
    "Pending",
    "Rejected"
]


work_modes = [
    "Office",
    "Remote",
    "Hybrid"
]


project_status = [
    "Active",
    "Completed",
    "On Hold"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_joining_date():
    start = date(2018, 1, 1)
    end = date(2025, 1, 1)

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))

# ============================================================
# INSERT DEPARTMENTS
# ============================================================

for i, dept in enumerate(departments, start=1):
    cursor.execute(
        """
        INSERT INTO departments(
            department_id,
            name
        )
        VALUES (?,?)
        """,
        (i, dept),
    )


# ============================================================
# GENERATE EMPLOYEES
# ============================================================

employee_department = {}

manager_ids = {}

employee_id = 1

for dept_id, dept_name in enumerate(departments, start=1):

    # Create one manager/head first
    manager_name = fake.name()

    manager_email = (
        manager_name.lower()
        .replace(" ", ".")
        .replace("'", "")
        + "@technova.com"
    )

    joining_date = random_joining_date()

    manager_title = job_titles[dept_name][-1][0]

    min_salary = job_titles[dept_name][-1][1]
    max_salary = job_titles[dept_name][-1][2]

    manager_salary = random.randint(min_salary, max_salary)

    cursor.execute(
        """
        INSERT INTO employees
        (
            employee_id,
            name,
            email,
            department_id,
            job_title,
            joining_date,
            salary,
            manager_id
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            employee_id,
            manager_name,
            manager_email,
            dept_id,
            manager_title,
            joining_date.isoformat(),
            manager_salary,
            None,
        ),
    )

    manager_ids[dept_id] = employee_id

    employee_department[employee_id] = dept_id

    employee_id += 1

    # Create remaining employees

    for _ in range(7):

        emp_name = fake.name()

        emp_email = (
            emp_name.lower()
            .replace(" ", ".")
            .replace("'", "")
            + "@technova.com"
        )

        title, low, high = random.choice(
            job_titles[dept_name][:-1]
        )

        salary = random.randint(low, high)

        joining = random_joining_date()

        cursor.execute(
            """
            INSERT INTO employees
            (
                employee_id,
                name,
                email,
                department_id,
                job_title,
                joining_date,
                salary,
                manager_id
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                employee_id,
                emp_name,
                emp_email,
                dept_id,
                title,
                joining.isoformat(),
                salary,
                manager_ids[dept_id],
            ),
        )

        employee_department[employee_id] = dept_id

        employee_id += 1


# ============================================================
# UPDATE DEPARTMENT HEADS
# ============================================================

for dept_id, manager in manager_ids.items():

    cursor.execute(
        """
        UPDATE departments
        SET head_employee_id=?
        WHERE department_id=?
        """,
        (
            manager,
            dept_id,
        ),
    )


# ============================================================
# GENERATE PROJECTS
# ============================================================

project_id = 1

for project in project_names:

    dept = random.randint(1, 6)

    budget = random.randint(
        1000000,
        10000000,
    )

    status = random.choice(project_status)

    cursor.execute(
        """
        INSERT INTO projects
        (
            project_id,
            project_name,
            department_id,
            status,
            budget
        )
        VALUES(?,?,?,?,?)
        """,
        (
            project_id,
            project,
            dept,
            status,
            budget,
        ),
    )

    project_id += 1

# ============================================================
# ASSIGN EMPLOYEES TO PROJECTS
# ============================================================

for emp_id, dept_id in employee_department.items():

    cursor.execute(
        """
        SELECT project_id
        FROM projects
        WHERE department_id = ?
        """,
        (dept_id,),
    )

    dept_projects = [row[0] for row in cursor.fetchall()]

    if not dept_projects:
        continue

    assigned = random.sample(
        dept_projects,
        k=min(random.randint(1, 3), len(dept_projects)),
    )

    for project in assigned:

        cursor.execute(
            """
            INSERT OR IGNORE INTO employee_projects
            (
                employee_id,
                project_id
            )
            VALUES (?,?)
            """,
            (
                emp_id,
                project,
            ),
        )


# ============================================================
# PERFORMANCE REVIEWS
# ============================================================

review_id = 1

for emp_id in employee_department.keys():

    cursor.execute(
        """
        SELECT job_title
        FROM employees
        WHERE employee_id=?
        """,
        (emp_id,),
    )

    title = cursor.fetchone()[0]

    if "Manager" in title or "Lead" in title:
        rating = round(random.uniform(4.2, 5.0), 1)

    elif "Senior" in title:
        rating = round(random.uniform(3.8, 4.8), 1)

    else:
        rating = round(random.uniform(3.0, 4.8), 1)

    training = random.random() < 0.9

    cursor.execute(
        """
        INSERT INTO performance_reviews
        (
            review_id,
            employee_id,
            review_year,
            rating,
            training_completed
        )
        VALUES (?,?,?,?,?)
        """,
        (
            review_id,
            emp_id,
            2025,
            rating,
            training,
        ),
    )

    review_id += 1


# ============================================================
# LEAVE REQUESTS
# ============================================================

leave_id = 1

for emp_id in employee_department.keys():

    total = random.randint(0, 4)

    for _ in range(total):

        start = fake.date_between(
            start_date="-1y",
            end_date="today",
        )

        duration = random.randint(1, 5)

        end = start + timedelta(days=duration)

        cursor.execute(
            """
            INSERT INTO leave_requests
            (
                leave_id,
                employee_id,
                leave_type,
                start_date,
                end_date,
                status
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                leave_id,
                emp_id,
                random.choice(leave_types),
                start.isoformat(),
                end.isoformat(),
                random.choice(leave_status),
            ),
        )

        leave_id += 1


# ============================================================
# ATTENDANCE
# ============================================================

attendance_id = 1

for emp_id in employee_department.keys():

    for _ in range(10):

        attendance_date = fake.date_between(
            start_date="-30d",
            end_date="today",
        )

        cursor.execute(
            """
            INSERT INTO attendance
            (
                attendance_id,
                employee_id,
                date,
                work_mode,
                hours_worked
            )
            VALUES (?,?,?,?,?)
            """,
            (
                attendance_id,
                emp_id,
                attendance_date.isoformat(),
                random.choice(work_modes),
                round(random.uniform(7.0, 9.5), 1),
            ),
        )

        attendance_id += 1


# ============================================================
# COMMIT
# ============================================================

conn.commit()

print("=" * 50)
print("TechNova Enterprise Database Created Successfully")
print("=" * 50)

print(f"Departments           : {len(departments)}")
print(f"Employees             : {len(employee_department)}")
print(f"Projects              : {len(project_names)}")
print(f"Performance Reviews   : {review_id-1}")
print(f"Leave Requests        : {leave_id-1}")
print(f"Attendance Records    : {attendance_id-1}")

print("\nDatabase Location:")
print(DATABASE_PATH)

conn.close()