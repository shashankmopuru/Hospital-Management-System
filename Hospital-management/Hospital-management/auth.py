# auth.py
import sqlite3
from bcrypt import checkpw, hashpw, gensalt

# Function to validate staff login
def validate_staff(username, password):
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT password, role FROM staff_login WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and checkpw(password.encode(), result[0]):
        return result[1]  # Return the role if password matches
    return None

# Function to validate patient login
def validate_patient(username, password):
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM patient_login WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and checkpw(password.encode(), result[0]):
        return True  # Password matches
    return False

# Function to register new staff
def register_staff(id, username, password, role):
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    hashed_password = hashpw(password.encode(), gensalt())
    
    try:
        cursor.execute("INSERT INTO staff_login (id, username, password, role) VALUES (?, ?, ?, ?)", 
                       (id, username, hashed_password, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists or ID conflict

# Function to register new patient
def register_patient(id, username, password):
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    hashed_password = hashpw(password.encode(), gensalt())
    
    try:
        cursor.execute("INSERT INTO patient_login (id, username, password) VALUES (?, ?, ?)", 
                       (id, username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists or ID conflict
