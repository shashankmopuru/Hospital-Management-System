import sqlite3
import bcrypt

# Connect to the database
conn = sqlite3.connect('hospital_management.db')
cursor = conn.cursor()

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Sample staff users with detailed information
staff_users = [
    {'id': 'a001', 'username': 'admin1', 'password': 'admin123', 'role': 'Admin', 'name': 'Admin User', 'phone': '555-0000', 'email': 'admin@example.com'},
    {'id': 'd001', 'username': 'doctor1', 'password': 'doctor123', 'role': 'Doctor', 'name': 'Dr. Smith', 'phone': '555-0001', 'email': 'doctor@example.com'},
    {'id': 'n001', 'username': 'nurse1', 'password': 'nurse123', 'role': 'Nurse', 'name': 'Nurse Jones', 'phone': '555-0002', 'email': 'nurse@example.com'},
    {'id': 'r001', 'username': 'reception1', 'password': 'reception123', 'role': 'Receptionist', 'name': 'Receptionist Brown', 'phone': '555-0003', 'email': 'receptionist@example.com'}
]

# Sample patients
patient_users = [
    {'id': 'p001', 'username': 'patient1', 'password': 'patient123', 'name': 'John Doe', 'phone': '1234567890', 'email': 'john@example.com', 'age': 30, 'ailment': 'Fever'},
    {'id': 'p002', 'username': 'patient2', 'password': 'patient123', 'name': 'Jane Smith', 'phone': '0987654321', 'email': 'jane@example.com', 'age': 25, 'ailment': 'Cough'}
]

# Insert sample staff users
for user in staff_users:
    hashed_password = hash_password(user['password'])
    cursor.execute("INSERT INTO staff_login (id, username, password, role) VALUES (?, ?, ?, ?)", (user['id'], user['username'], hashed_password, user['role']))
    cursor.execute(f"INSERT INTO {user['role'].lower()}s (id, name, phone, email) VALUES (?, ?, ?, ?)", (user['id'], user['name'], user['phone'], user['email']))

# Insert sample patients
for patient in patient_users:
    hashed_password = hash_password(patient['password'])
    cursor.execute("INSERT INTO patient_login (id, username, password) VALUES (?, ?, ?)", (patient['id'], patient['username'], hashed_password))
    cursor.execute("INSERT INTO patients (id, name, phone, email, age, ailment) VALUES (?, ?, ?, ?, ?, ?)", 
                   (patient['id'], patient['name'], patient['phone'], patient['email'], patient['age'], patient['ailment']))

# Commit and close
conn.commit()
conn.close()

print("Sample users, including admin, added successfully.")
