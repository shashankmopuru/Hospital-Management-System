import sqlite3

conn = sqlite3.connect('hospital_management.db')
cursor = conn.cursor()

cursor.executescript("""
-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Drop existing tables if any
DROP TABLE IF EXISTS patient_login;
DROP TABLE IF EXISTS staff_login;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS nurses;
DROP TABLE IF EXISTS receptionists;
DROP TABLE IF EXISTS admins;

-- Create tables
CREATE TABLE IF NOT EXISTS doctors (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    specialization TEXT
);

CREATE TABLE IF NOT EXISTS nurses (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    department TEXT
);

CREATE TABLE IF NOT EXISTS receptionists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS admins (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    age INTEGER,
    ailment TEXT,
    department TEXT,
    diagnosis TEXT,
    treatment_notes TEXT
);

-- Staff login table with foreign key
CREATE TABLE IF NOT EXISTS staff_login (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Doctor', 'Nurse', 'Receptionist')),
    FOREIGN KEY (id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES nurses(id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES receptionists(id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES admins(id) ON DELETE CASCADE
);

-- Patient login table with foreign key
CREATE TABLE IF NOT EXISTS patient_login (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES patients(id) ON DELETE CASCADE
);
""")

conn.commit()
conn.close()
