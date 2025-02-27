import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

# Initialize Database
def initialize_db():
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicines (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        dose TEXT,
                        frequency TEXT,
                        days TEXT,
                        times TEXT,
                        status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

initialize_db()

# Fetch all medicines
def get_medicines():
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to refresh the display
def refresh_display():
    # Clear the display frame
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    # Display today's date
    today = datetime.today().strftime('%A, %B %d, %Y')
    tk.Label(display_frame, text=today, font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Fetch and display medicines
    medicines = get_medicines()
    if medicines:
        for med in medicines:
            med_id, name, dose, frequency, days, times, status = med
            tk.Label(display_frame, text=f"Medicine: {name}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
            tk.Label(display_frame, text=f"Dose: {dose}", font=("Arial", 10), bg="#f0f0f0").pack()
            
            # Display dose times
            times_list = times.split(",")
            for i, time in enumerate(times_list):
                tk.Label(display_frame, text=f"Dose {i+1}: {time.strip()}", font=("Arial", 10), bg="#f0f0f0").pack()
            
            # Add buttons for delete and edit
            button_frame = tk.Frame(display_frame, bg="#f0f0f0")
            button_frame.pack()
            tk.Button(button_frame, text="Delete", command=lambda med_id=med_id: delete_medicine(med_id), bg="red", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Edit", command=lambda med_id=med_id: edit_medicine(med_id), bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
            
            # Add a separator
            tk.Label(display_frame, text="-----------------------------", bg="#f0f0f0").pack()
    else:
        tk.Label(display_frame, text="No medicines added.", font=("Arial", 12, "italic"), bg="#f0f0f0").pack()

# Function to delete medicine
def delete_medicine(med_id):
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
    conn.commit()
    conn.close()
    refresh_display()

# Function to edit medicine (placeholder for now)
def edit_medicine(med_id):
    print(f"Editing medicine with ID: {med_id}")  # Placeholder for edit functionality

# UI Setup
root = tk.Tk()
root.title("Medicine Reminder")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Title Label
tk.Label(root, text="Medicine Reminder", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Display Frame (to show medicines)
display_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
display_frame.pack(pady=20)

# Refresh Display (populate the display frame with medicines)
refresh_display()

# Buttons for Refresh and Add Medicine
tk.Button(root, text="Refresh", command=refresh_display, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Add Medicine", command=lambda: print("Open Add Medicine Window"), bg="#007BFF", fg="white").pack(pady=5)

# Start the main event loop
root.mainloop()