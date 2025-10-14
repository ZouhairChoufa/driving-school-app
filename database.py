import sqlite3
import hashlib
import os

DB_FILE = 'driving_school.db'

def setup_database():
    """Creates and safely upgrades the database tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE, company_id TEXT NOT NULL,
        password_hash TEXT NOT NULL, role TEXT NOT NULL
    )''')
    
    # Create clients table
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, address TEXT, phone TEXT, 
        license_type TEXT, image_path TEXT, company_name TEXT, company_id INTEGER)''')
    
    # Create employees table with all columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, birthday TEXT, cin TEXT, 
        phone TEXT, address TEXT, image_path TEXT)''')
    
    # Create admin_profile table
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin_profile (
        id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, phone TEXT, address TEXT, 
        image_path TEXT, company_name TEXT, company_id INTEGER, password_hash TEXT, fax TEXT, email TEXT)''')
    
    def add_column_if_not_exists(table, column, col_type):
        try:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]
            if column not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        except Exception as e:
            print(f"Could not add column {column} to {table}: {e}")

    # Safely add columns for clients table
    add_column_if_not_exists("clients", "birthday", "TEXT")
    add_column_if_not_exists("clients", "cin", "TEXT")
    add_column_if_not_exists("clients", "hours_practice", "INTEGER")
    add_column_if_not_exists("clients", "hours_theory", "INTEGER")
    add_column_if_not_exists("clients", "vehicle_matricule", "TEXT")
    add_column_if_not_exists("clients", "exam_success_date", "TEXT")
    add_column_if_not_exists("clients", "monitor_name", "TEXT") 
    
    # Safely add columns for employees table
    add_column_if_not_exists("employees", "birthday", "TEXT")
    add_column_if_not_exists("employees", "cin", "TEXT")

    # Safely add columns for admin_profile table
    add_column_if_not_exists("admin_profile", "fax", "TEXT")
    add_column_if_not_exists("admin_profile", "email", "TEXT")
    add_column_if_not_exists("admin_profile", "password_hash", "TEXT")

    conn.commit()
    conn.close()

# --- User and Login Functions ---
def check_if_admin_exists(company_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE company_id = ? AND role = 'Admin'", (company_id,))
    data = cursor.fetchone()
    conn.close()
    return data is not None

def create_user(first_name, last_name, username, company_id, password):
    role = 'Admin' if not check_if_admin_exists(company_id) else 'Employee'
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("INSERT INTO users (first_name, last_name, username, company_id, password_hash, role) VALUES (?, ?, ?, ?, ?, ?)", 
                     (first_name, last_name, username, company_id, hashed_password, role))
        conn.commit()
    finally:
        conn.close()

def check_login(username, password):
    if username == '5704' and password == 'admin':
        if not get_admin_profile():
            update_admin_profile({
                'first_name': 'Main', 'last_name': 'Admin', 'company_name': 'Auto Ecole Abd El Karim',
                'company_id': '5704', 'address': '', 'phone': '', 'fax': '', 'email': ''
            })
        return 'Admin'

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        stored_hash, role = user_data
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input == stored_hash:
            return role
    return None

# --- Admin Profile Functions ---
def get_admin_profile():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_profile WHERE id=1")
    data = cursor.fetchone()
    conn.close()
    return data

def update_admin_profile(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    exists = cursor.execute("SELECT id FROM admin_profile WHERE id=1").fetchone()
    if exists:
        sql = "UPDATE admin_profile SET first_name=?, last_name=?, company_name=?, company_id=?, address=?, phone=?, fax=?, email=?"
        params = (data['first_name'], data['last_name'], data['company_name'], data['company_id'], data['address'], data['phone'], data['fax'], data['email'])
        if data.get('image_path'):
            sql += ", image_path=?"
            params += (data['image_path'],)
        sql += " WHERE id=1"
        cursor.execute(sql, params)
    else:
        cursor.execute("INSERT INTO admin_profile (id, first_name, last_name, phone, address, image_path, company_name, company_id, fax, email) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (data['first_name'], data['last_name'], data['phone'], data['address'], data.get('image_path'), data['company_name'], data['company_id'], data['fax'], data['email']))
    conn.commit()
    conn.close()

# --- Client Functions ---
def get_clients(search_term=""):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if search_term:
        query = "SELECT * FROM clients WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR cin LIKE ?"
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    else:
        cursor.execute("SELECT * FROM clients")
    data = cursor.fetchall()
    conn.close()
    return data

def get_client_by_id(client_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def add_client(data):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO clients (first_name, last_name, address, birthday, cin, phone, hours_practice, hours_theory, vehicle_matricule, monitor_name, exam_success_date, license_type, image_path, company_name, company_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                 (data['first_name'], data['last_name'], data['address'], data['birthday'], data['cin'], data['phone'], data['hours_practice'], data['hours_theory'], data['vehicle_matricule'], data['monitor_name'], data['exam_success_date'], data['license_type'], data['image_path'], data['company_name'], data['company_id']))
    conn.commit()
    conn.close()

def update_client(client_id, data):
    conn = sqlite3.connect(DB_FILE)
    sql_base = "UPDATE clients SET first_name=?, last_name=?, address=?, birthday=?, cin=?, phone=?, hours_practice=?, hours_theory=?, vehicle_matricule=?, monitor_name=?, exam_success_date=?, license_type=?"
    params_base = (data['first_name'], data['last_name'], data['address'], data['birthday'], data['cin'], data['phone'], data['hours_practice'], data['hours_theory'], data['vehicle_matricule'], data['monitor_name'], data['exam_success_date'], data['license_type'])
    if data.get('image_path'):
        sql = sql_base + ", image_path=? WHERE id=?"
        params = params_base + (data['image_path'], client_id)
    else:
        sql = sql_base + " WHERE id=?"
        params = params_base + (client_id,)
    conn.execute(sql, params)
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = sqlite3.connect(DB_FILE); conn.execute("DELETE FROM clients WHERE id=?", (client_id,)); conn.commit(); conn.close()

# --- Employee Functions ---
def get_employees():
    conn = sqlite3.connect(DB_FILE); data = conn.execute("SELECT * FROM employees").fetchall(); conn.close(); return data

def get_employee_by_id(emp_id):
    conn = sqlite3.connect(DB_FILE); data = conn.execute("SELECT * FROM employees WHERE id=?", (emp_id,)).fetchone(); conn.close(); return data

def add_employee(data):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO employees (first_name, last_name, birthday, cin, phone, address, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                 (data['first_name'], data['last_name'], data['birthday'], data['cin'], data['phone'], data['address'], data['image_path']))
    conn.commit(); conn.close()

def update_employee(emp_id, data):
    conn = sqlite3.connect(DB_FILE)
    sql = "UPDATE employees SET first_name=?, last_name=?, birthday=?, cin=?, phone=?, address=?"
    params = (data['first_name'], data['last_name'], data['birthday'], data['cin'], data['phone'], data['address'])
    if data.get('image_path'):
        sql += ", image_path=?"
        params += (data['image_path'],)
    sql += " WHERE id=?"
    params += (emp_id,)
    conn.execute(sql, params)
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = sqlite3.connect(DB_FILE); conn.execute("DELETE FROM employees WHERE id=?", (emp_id,)); conn.commit(); conn.close()

# --- Dashboard Function ---
def get_dashboard_stats():
    conn = sqlite3.connect(DB_FILE)
    total_clients = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    total_employees = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    conn.close(); return total_clients, total_employees
