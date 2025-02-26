import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

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

