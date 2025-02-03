import tkinter as tk
from tkinter import messagebox
from auth import validate_staff, validate_patient, register_staff, register_patient
import sqlite3

current_role = None
current_user = None

# Setup main application window
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("450x650")

# Define entry fields as global
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")

# Function to handle login based on selected role
def login(role):
    global current_role, current_user
    username = entry_username.get()
    password = entry_password.get()
    
    if role == "Staff":
        role = validate_staff(username, password)
        if role:
            current_role = role
            current_user = username
            messagebox.showinfo("Login Success", f"Welcome {role}")
            show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    elif role == "Patient":
        if validate_patient(username, password):
            current_role = "Patient"
            current_user = username
            messagebox.showinfo("Login Success", "Welcome Patient")
            show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Function to display patient information
def display_patient_info():
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    top = tk.Toplevel(root)
    top.title("Patient Information")

    headers = ["ID", "Name", "Phone", "Email", "Age", "Ailment", "Department", "Diagnosis", "Treatment Notes"]
    for header in headers:
        tk.Label(top, text=header, font=("Arial", 10, "bold")).grid(row=0, column=headers.index(header), padx=5, pady=5)

    for index, patient in enumerate(patients):
        for col_index, value in enumerate(patient):
            tk.Label(top, text=value).grid(row=index + 1, column=col_index, padx=5, pady=5)

# Function to create a new staff member
def create_staff():
    if current_role != "Admin":
        return

    def save_staff():
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        username = entry_username.get()
        password = entry_password.get()
        role = var_role.get()

        staff_id = generate_staff_id(role)
        if register_staff(staff_id, username, password, role):
            conn = sqlite3.connect('hospital_management.db')
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {role.lower()}s (id, name, phone, email) VALUES (?, ?, ?, ?)", 
                           (staff_id, name, phone, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Staff member '{username}' registered successfully")
        else:
            messagebox.showerror("Error", "Failed to register staff member. Username may already exist.")

    top = tk.Toplevel(root)
    top.title("Create New Staff")

    tk.Label(top, text="Name").pack(pady=5)
    entry_name = tk.Entry(top)
    entry_name.pack(pady=5)

    tk.Label(top, text="Phone").pack(pady=5)
    entry_phone = tk.Entry(top)
    entry_phone.pack(pady=5)

    tk.Label(top, text="Email").pack(pady=5)
    entry_email = tk.Entry(top)
    entry_email.pack(pady=5)

    tk.Label(top, text="Username").pack(pady=5)
    entry_username = tk.Entry(top)
    entry_username.pack(pady=5)

    tk.Label(top, text="Password").pack(pady=5)
    entry_password = tk.Entry(top, show="*")
    entry_password.pack(pady=5)

    var_role = tk.StringVar(value="Nurse")
    tk.Label(top, text="Select Role").pack(pady=5)
    tk.OptionMenu(top, var_role, "Admin", "Doctor", "Nurse", "Receptionist").pack(pady=5)

    tk.Button(top, text="Create Staff", command=save_staff).pack(pady=10)

# Function to generate staff ID
def generate_staff_id(role):
    prefix = {'Admin': 'a', 'Doctor': 'd', 'Nurse': 'n', 'Receptionist': 'r'}.get(role, 'u')
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {role.lower()}s")
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"{prefix}{count:03}"

# Function to register a new patient
def add_patient():
    if current_role not in ["Admin", "Receptionist"]:
        return

    def save_patient():
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        age = int(entry_age.get())
        ailment = entry_ailment.get()
        username = entry_username.get()
        password = entry_password.get()

        patient_id = generate_patient_id()
        if register_patient(patient_id, username, password):
            conn = sqlite3.connect('hospital_management.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patients (id, name, phone, email, age, ailment) VALUES (?, ?, ?, ?, ?, ?)", 
                           (patient_id, name, phone, email, age, ailment))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Patient '{username}' registered successfully")
        else:
            messagebox.showerror("Error", "Failed to register patient. Username may already exist.")

    top = tk.Toplevel(root)
    top.title("Register New Patient")

    tk.Label(top, text="Name").pack(pady=5)
    entry_name = tk.Entry(top)
    entry_name.pack(pady=5)

    tk.Label(top, text="Phone").pack(pady=5)
    entry_phone = tk.Entry(top)
    entry_phone.pack(pady=5)

    tk.Label(top, text="Email").pack(pady=5)
    entry_email = tk.Entry(top)
    entry_email.pack(pady=5)

    tk.Label(top, text="Age").pack(pady=5)
    entry_age = tk.Entry(top)
    entry_age.pack(pady=5)

    tk.Label(top, text="Ailment").pack(pady=5)
    entry_ailment = tk.Entry(top)
    entry_ailment.pack(pady=5)

    tk.Label(top, text="Username").pack(pady=5)
    entry_username = tk.Entry(top)
    entry_username.pack(pady=5)

    tk.Label(top, text="Password").pack(pady=5)
    entry_password = tk.Entry(top, show="*")
    entry_password.pack(pady=5)

    tk.Button(top, text="Save Patient", command=save_patient).pack(pady=10)

# Function to generate patient ID
def generate_patient_id():
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"p{count:03}"

# Function to update patient's diagnosis and treatment notes
def update_patient_diagnosis():
    if current_role != "Doctor":
        return

    def save_update():
        patient_id = entry_patient_id.get()
        diagnosis = entry_diagnosis.get()
        treatment_notes = entry_treatment_notes.get()

        conn = sqlite3.connect('hospital_management.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET diagnosis=?, treatment_notes=? WHERE id=?", 
                       (diagnosis, treatment_notes, patient_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient's diagnosis and treatment notes updated successfully")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Update Patient Diagnosis")

    tk.Label(top, text="Patient ID").pack(pady=5)
    entry_patient_id = tk.Entry(top)
    entry_patient_id.pack(pady=5)

    tk.Label(top, text="Diagnosis").pack(pady=5)
    entry_diagnosis = tk.Entry(top)
    entry_diagnosis.pack(pady=5)

    tk.Label(top, text="Treatment Notes").pack(pady=5)
    entry_treatment_notes = tk.Entry(top)
    entry_treatment_notes.pack(pady=5)

    tk.Button(top, text="Update", command=save_update).pack(pady=10)

# Function to update patient's department (for Nurse)
def update_patient_department():
    if current_role != "Nurse":
        return

    def save_update():
        patient_id = entry_patient_id.get()
        department = entry_department.get()

        conn = sqlite3.connect('hospital_management.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET department=? WHERE id=?", 
                       (department, patient_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient's department updated successfully")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Update Patient Department")

    tk.Label(top, text="Patient ID").pack(pady=5)
    entry_patient_id = tk.Entry(top)
    entry_patient_id.pack(pady=5)

    tk.Label(top, text="Department").pack(pady=5)
    entry_department = tk.Entry(top)
    entry_department.pack(pady=5)

    tk.Button(top, text="Update", command=save_update).pack(pady=10)

# Function to view all staff information
def view_all_receptionist():
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receptionists")
    staff = cursor.fetchall()
    conn.close()

    top = tk.Toplevel(root)
    top.title("Receptionist Information")

    headers = ["ID", "Name", "Phone","Email"]
    for header in headers:
        tk.Label(top, text=header, font=("Arial", 10, "bold")).grid(row=0, column=headers.index(header), padx=5, pady=5)

    for index, member in enumerate(staff):
        for col_index, value in enumerate(member):
            tk.Label(top, text=value).grid(row=index + 1, column=col_index, padx=5, pady=5)

def view_all_nurse():
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nurses;")
    staff = cursor.fetchall()
    conn.close()

    top = tk.Toplevel(root)
    top.title("Nurse Information")

    headers = ["ID", "Name", "Phone","Email","department"]
    for header in headers:
        tk.Label(top, text=header, font=("Arial", 10, "bold")).grid(row=0, column=headers.index(header), padx=5, pady=5)

    for index, member in enumerate(staff):
        for col_index, value in enumerate(member):
            tk.Label(top, text=value).grid(row=index + 1, column=col_index, padx=5, pady=5)

def view_all_doctor():
    conn = sqlite3.connect('hospital_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors;")
    staff = cursor.fetchall()
    conn.close()

    top = tk.Toplevel(root)
    top.title("Doctor Information")

    headers = ["ID", "Name", "Phone","Email","Specialization"]
    for header in headers:
        tk.Label(top, text=header, font=("Arial", 10, "bold")).grid(row=0, column=headers.index(header), padx=5, pady=5)

    for index, member in enumerate(staff):
        for col_index, value in enumerate(member):
            tk.Label(top, text=value).grid(row=index + 1, column=col_index, padx=5, pady=5)


# Main menu for each role
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text=f"Welcome, {current_role}", font=("Arial", 14)).pack(pady=10)

    if current_role == "Doctor":
        tk.Button(root, text="Update Patient Diagnosis", command=update_patient_diagnosis).pack(pady=5)
        tk.Button(root, text="Show All Patient Information", command=display_patient_info).pack(pady=5)
        tk.Button(root, text="Show All Nurse Information", command=view_all_nurse).pack(pady=5) 

    elif current_role == "Nurse":
        tk.Button(root, text="Update Patient Department", command=update_patient_department).pack(pady=5)
        tk.Button(root, text="Show All Patient Information", command=display_patient_info).pack(pady=5)

    elif current_role == "Receptionist":
        tk.Button(root, text="Register New Patient", command=add_patient).pack(pady=5)
        tk.Button(root, text="Show All Nurse Information", command=view_all_nurse).pack(pady=5) 
        tk.Button(root, text="Show All Doctors Information", command=view_all_doctor).pack(pady=5) 

    elif current_role == "Admin":
        tk.Button(root, text="Create New Staff", command=create_staff).pack(pady=5)
        tk.Button(root, text="View All Patients", command=display_patient_info).pack(pady=5)
        tk.Button(root, text="Show All Nurse Information", command=view_all_nurse).pack(pady=5) 
        tk.Button(root, text="Show All Doctors Information", command=view_all_doctor).pack(pady=5) 
        tk.Button(root, text="Show All Receptionist Information", command=view_all_receptionist).pack(pady=5) 

    tk.Button(root, text="Logout", command=logout).pack(pady=10)

# Logout function
def logout():
    global current_role, current_user
    current_role = None
    current_user = None
    show_login_screen()

# Show login screen with separate options for staff and patients
def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Hospital Management System", font=("Arial", 18)).pack(pady=20)
    tk.Button(root, text="Patient Login", command=lambda: show_role_login("Patient")).pack(pady=10)
    tk.Button(root, text="Staff Login", command=lambda: show_role_login("Staff")).pack(pady=10)

# Show login screen for selected role
def show_role_login(role):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text=f"{role} Login", font=("Arial", 18)).pack(pady=20)

    tk.Label(root, text="Username").pack(pady=5)
    global entry_username
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    tk.Button(root, text="Login", command=lambda: login(role)).pack(pady=10)
    tk.Button(root, text="Back", command=show_login_screen).pack(pady=5)

# Start the application
show_login_screen()
root.mainloop()
