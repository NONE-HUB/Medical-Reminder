import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from homepage import login_client, open_signup

# Database setup
def dataset_db():
    conn = sqlite3.connect("client.db")
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
            status TEXT,  -- "Taken" or "Missed"
            FOREIGN KEY(client_id) REFERENCES client(id)
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the tables
dataset_db()

# Add medication history to the database
def add_medication_history(client_id, medication_name, dosage, scheduled_time, taken_time, status):
    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medication_history (client_id, medication_name, dosage, scheduled_time, taken_time, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (client_id, medication_name, dosage, scheduled_time, taken_time, status))
    conn.commit()
    conn.close()

# Fetch medication history from the database
def get_medication_history(client_id):
    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medication_history WHERE client_id=?", (client_id,))
    history = cursor.fetchall()
    conn.close()
    return history

# Function to mark medicine as taken or missed
def mark_medication(client_id, medication_name, scheduled_time, status):
    taken_time = "Now" if status == "Taken" else "Missed"
    add_medication_history(client_id, medication_name, "1 tablet", scheduled_time, taken_time, status)
    messagebox.showinfo("Success", f"Medication marked as {status}!")

# To open adherence tracking window
def open_adherence_tracking(parent_window, client_id):
    adherence_window = tk.Toplevel(parent_window)
    adherence_window.title("Adherence Tracking")
    adherence_window.geometry('600x400')
    history = get_medication_history(client_id)
    tk.Label(adherence_window, text="Medication History", font=("Arial", 16)).pack()
    headers = ["Medication", "Dosage", "Scheduled Time", "Taken Time", "Status"]
    for i, header in enumerate(headers):
        tk.Label(adherence_window, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i)

    # Displaying every record
    for row, record in enumerate(history, start=1):
        medication_name, dosage, scheduled_time, taken_time, status = record[2:7]
        tk.Label(adherence_window, text=medication_name).grid(row=row, column=0)
        tk.Label(adherence_window, text=dosage).grid(row=row, column=1)
        tk.Label(adherence_window, text=scheduled_time).grid(row=row, column=2)
        tk.Label(adherence_window, text=taken_time).grid(row=row, column=3)
        tk.Label(adherence_window, text=status).grid(row=row, column=4)

    # Buttons to mark medication as taken or missed
    tk.Button(adherence_window, text="Mark as Taken", command=lambda: mark_medication(client_id, "Paracetamol", "08:00 AM", "Taken")).grid(row=1, column=5)
    tk.Button(adherence_window, text="Mark as Missed", command=lambda: mark_medication(client_id, "Paracetamol", "08:00 AM", "Missed")).grid(row=2, column=5)

# Main application window
root = tk.Tk()
root.title("Login Page")
root.geometry("800x600")

# Background
bg_image = Image.open(r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\bg.png")
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

tk.Label(root, text="Email").pack()
login_email = tk.Entry(root)
login_email.pack()

tk.Label(root, text="Password").pack()
login_Password = tk.Entry(root, show="*")
login_Password.pack()

tk.Button(root, text="Login", command=login_client).pack()
tk.Button(root, text="Sign up", command=open_signup).pack()

root.mainloop()