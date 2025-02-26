import tkinter as tk
from tkinter import messagebox
import sqlite3

def dataset_db():
    conn= sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS client(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   email TEXT UNIQUE,
                   First_Name TEXT,
                   Last_Name TEXT,
                   Password TEXT
                   )
                ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS medication_history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   client_id INTEGER,
                   medication_name TEXT,
                   dosage TEXT,
                   scheduled_time TEXT,
                   taken_time TEXT,
                   status TEXT, #"Taken" or " Missed")
                   FOREIGN KEY(client_id) REFERENCES client(id)
                   )
                ''')
    conn.commit()
    conn.close()
    
def add_medication_history(client_id, medication_name, dosage, scheduled_time, taken_time, status):
    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medication_history, dosage, scheduled_time, taken_time, status))
        VALUES (?, ?, ?, ?, ?, ?)
    ''',(client_id, medication_name, dosage, scheduled_time, taken_time, status))
    conn.commit
    conn.close()

def get_medication_history (client_id):
    conn = sqlite3.connect("client.db")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medication_histroy WHERE client_id=?", (client_id,))
    history = cursor.fetchall()
    conn.close()
    return history

