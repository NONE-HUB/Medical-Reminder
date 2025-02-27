import tkinter as tk
from tkinter import messagebox, ttk
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

# Convert 24-hour format to AM/PM
def format_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        return time_str

# Function to show/hide days based on frequency selection
def update_days_visibility(event):
    if frequency_var.get() == "Selected Days":
        day_frame.pack()
    else:
        day_frame.pack_forget()

# Function to show/hide dose time selection based on dose
def update_dose_times(event):
    selected_dose = int(dose_var.get()[0])
    for i in range(3):
        if i < selected_dose:
            time_labels[i].pack()
            time_vars[i].pack()
        else:
            time_labels[i].pack_forget()
            time_vars[i].pack_forget()

# Function to add medicine
def add_medicine():
    name = name_entry.get()
    dose = dose_var.get()
    frequency = frequency_var.get()
    days = ",".join([day for day, var in days_vars.items() if var.get()]) if frequency == "Selected Days" else ""
    selected_dose = int(dose[0])
    times = ",".join([time_vars[i].get() for i in range(selected_dose)])

    if not (name and dose and frequency and times):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medicines (name, dose, frequency, days, times) VALUES (?, ?, ?, ?, ?)",
                   (name, dose, frequency, days, times))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Medicine added successfully!")
    add_window.destroy()

# Add Medicine Window
def open_add_window():
    global add_window, name_entry, dose_var, frequency_var, days_vars, time_vars, time_labels, day_frame
    
    add_window = tk.Toplevel(root)
    add_window.title("Add Medicine")
    add_window.geometry("400x500")
    
    tk.Label(add_window, text="Medicine Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()
    
    tk.Label(add_window, text="Frequency:").pack()
    frequency_var = ttk.Combobox(add_window, values=["Daily", "Selected Days"])
    frequency_var.pack()
    frequency_var.bind("<<ComboboxSelected>>", update_days_visibility)
    
    days_vars = {}
    day_frame = tk.Frame(add_window)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        days_vars[day] = tk.IntVar()
        tk.Checkbutton(day_frame, text=day, variable=days_vars[day]).pack(side=tk.LEFT)
    
    tk.Label(add_window, text="Dose:").pack()
    dose_var = ttk.Combobox(add_window, values=["1 pill", "2 pills", "3 pills"])
    dose_var.pack()
    dose_var.bind("<<ComboboxSelected>>", update_dose_times)
    
    time_vars = []
    time_labels = []
    for i in range(3):
        time_labels.append(tk.Label(add_window, text=f"Dose {i+1} Time:"))
        time_vars.append(ttk.Combobox(add_window, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)]))
    
    tk.Button(add_window, text="Save", command=add_medicine, bg="green", fg="white").pack(pady=10)
    tk.Button(add_window, text="Cancel", command=add_window.destroy, bg="red", fg="white").pack()

# UI Setup
root = tk.Tk()
root.title("Medicine Reminder")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Medicine Reminder", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Add Medicine Button
tk.Button(root, text="Add Medicine", command=open_add_window, bg="#007BFF", fg="white").pack(pady=5)

root.mainloop()
