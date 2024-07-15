import sqlite3

# SQLite 데이터베이스 연결 (또는 생성)
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER,
    hire_date TEXT,
    salary REAL,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS EmployeeProjects (
    employee_id INTEGER,
    project_id INTEGER,
    role TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    PRIMARY KEY (employee_id, project_id)
)
''')

# 샘플 데이터 삽입
cursor.execute("INSERT INTO Departments (department_name) VALUES ('Human Resources')")
cursor.execute("INSERT INTO Departments (department_name) VALUES ('IT')")
cursor.execute("INSERT INTO Departments (department_name) VALUES ('Finance')")

cursor.execute("INSERT INTO Employees (first_name, last_name, department_id, hire_date, salary) VALUES ('John', 'Doe', 1, '2020-01-15', 60000)")
cursor.execute("INSERT INTO Employees (first_name, last_name, department_id, hire_date, salary) VALUES ('Jane', 'Smith', 2, '2019-03-10', 75000)")
cursor.execute("INSERT INTO Employees (first_name, last_name, department_id, hire_date, salary) VALUES ('Emily', 'Jones', 3, '2021-06-01', 50000)")

cursor.execute("INSERT INTO Projects (project_name, start_date, end_date) VALUES ('Project Alpha', '2021-01-01', '2021-12-31')")
cursor.execute("INSERT INTO Projects (project_name, start_date, end_date) VALUES ('Project Beta', '2022-01-01', '2022-12-31')")

cursor.execute("INSERT INTO EmployeeProjects (employee_id, project_id, role) VALUES (1, 1, 'Manager')")
cursor.execute("INSERT INTO EmployeeProjects (employee_id, project_id, role) VALUES (2, 2, 'Developer')")
cursor.execute("INSERT INTO EmployeeProjects (employee_id, project_id, role) VALUES (3, 1, 'Analyst')")

# 변경 사항 저장 및 연결 종료
conn.commit()
conn.close()

