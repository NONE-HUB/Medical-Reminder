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
    # Check if the number of medicines exceeds 5
    if len(get_medicines()) >= 5:
        messagebox.showerror("Error", "Only 5 medicines can be added!")
        return

    name = name_entry.get()  # Medicine name
    dose = dose_var.get()  # Dose (e.g., "1 pill", "2 pills")
    frequency = frequency_var.get()  # Frequency (e.g., "Daily", "Selected Days")
    
    # Collect selected days (if frequency is "Selected Days")
    days = ",".join([day for day, var in days_vars.items() if var.get()]) if frequency == "Selected Days" else ""
    
    # Collect times for each dose
    selected_dose = int(dose[0])  # Extract the number of doses (e.g., "1 pill" -> 1)
    times = ",".join([time_vars[i].get() for i in range(selected_dose)])
    
    # Validate inputs
    if not (name and dose and frequency and times):
        messagebox.showerror("Error", "Please fill all fields.")
        return
    
    # Insert into database
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medicines (name, dose, frequency, days, times) VALUES (?, ?, ?, ?, ?)",
                   (name, dose, frequency, days, times))
    conn.commit()
    conn.close()
    
    # Show success message
    messagebox.showinfo("Success", "Medicine added successfully!")
    
    # Close the "Add Medicine" window
    add_window.destroy()
    
    # Refresh the main screen
    refresh_display()

# Function to delete medicine
def delete_medicine(med_id):
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
    conn.commit()
    conn.close()
    refresh_display()

# Function to edit medicine
def edit_medicine(med_id):
    # Fetch the medicine details
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines WHERE id=?", (med_id,))
    med = cursor.fetchone()
    conn.close()

    # Open the edit window
    open_edit_window(med)

# Function to open the edit window
def open_edit_window(med):
    global edit_window, edit_name_entry, edit_dose_var, edit_frequency_var, edit_days_vars, edit_time_vars, edit_time_labels, edit_day_frame

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Medicine")
    edit_window.geometry("400x500")

    med_id, name, dose, frequency, days, times, status = med

    tk.Label(edit_window, text="Medicine Name:").pack()
    edit_name_entry = tk.Entry(edit_window)
    edit_name_entry.insert(0, name)
    edit_name_entry.pack()

    tk.Label(edit_window, text="Frequency:").pack()
    edit_frequency_var = ttk.Combobox(edit_window, values=["Daily", "Selected Days"])
    edit_frequency_var.set(frequency)
    edit_frequency_var.pack()
    edit_frequency_var.bind("<<ComboboxSelected>>", update_days_visibility)

    # Days selection (hidden initially)
    edit_days_vars = {}
    edit_day_frame = tk.Frame(edit_window)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        edit_days_vars[day] = tk.IntVar()
        if days and day in days.split(","):
            edit_days_vars[day].set(1)
        tk.Checkbutton(edit_day_frame, text=day, variable=edit_days_vars[day]).pack(side=tk.LEFT)

    if frequency == "Selected Days":
        edit_day_frame.pack()

    tk.Label(edit_window, text="Dose:").pack()
    edit_dose_var = ttk.Combobox(edit_window, values=["1 pill", "2 pills", "3 pills"])
    edit_dose_var.set(dose)
    edit_dose_var.pack()
    edit_dose_var.bind("<<ComboboxSelected>>", update_dose_times)

    # Time selection (initially hidden)
    edit_time_vars = []
    edit_time_labels = []
    times_list = times.split(",")
    for i in range(3):
        edit_time_labels.append(tk.Label(edit_window, text=f"Dose {i+1} Time:"))
        edit_time_vars.append(ttk.Combobox(edit_window, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)]))
        if i < len(times_list):
            edit_time_vars[i].set(times_list[i])
        edit_time_labels[i].pack()
        edit_time_vars[i].pack()

    tk.Button(edit_window, text="Save", command=lambda: save_edited_medicine(med_id), bg="green", fg="white").pack(pady=10)
    tk.Button(edit_window, text="Cancel", command=edit_window.destroy, bg="red", fg="white").pack()

# Function to save edited medicine
def save_edited_medicine(med_id):
    name = edit_name_entry.get()
    dose = edit_dose_var.get()
    frequency = edit_frequency_var.get()
    days = ",".join([day for day, var in edit_days_vars.items() if var.get()]) if frequency == "Selected Days" else ""
    selected_dose = int(dose[0])
    times = ",".join([edit_time_vars[i].get() for i in range(selected_dose)])

    if not (name and dose and frequency and times):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET name=?, dose=?, frequency=?, days=?, times=? WHERE id=?",
                   (name, dose, frequency, days, times, med_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Medicine updated successfully!")
    edit_window.destroy()
    refresh_display()

# Function to refresh the display
def refresh_display():
    for widget in display_frame.winfo_children():
        widget.destroy()
    
    today = datetime.today().strftime('%A, %B %d, %Y')
    tk.Label(display_frame, text=today, font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    
    medicines = get_medicines()
    if medicines:
        for med in medicines:
            med_id, name, dose, frequency, days, times, status = med
            tk.Label(display_frame, text=f"Medicine: {name}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
            tk.Label(display_frame, text=f"Dose: {dose}", font=("Arial", 10), bg="#f0f0f0").pack()
            
            times_list = times.split(",")
            for i, time in enumerate(times_list):
                formatted_time = format_time(time.strip())
                tk.Label(display_frame, text=f"{i+1}st Dose: {formatted_time}", font=("Arial", 10), bg="#f0f0f0").pack()
            
            # Add Delete and Edit buttons
            button_frame = tk.Frame(display_frame, bg="#f0f0f0")
            button_frame.pack()
            tk.Button(button_frame, text="Delete", command=lambda med_id=med_id: delete_medicine(med_id), bg="red", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Edit", command=lambda med_id=med_id: edit_medicine(med_id), bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
            
            tk.Label(display_frame, text="-----------------------------", bg="#f0f0f0").pack()
    else:
        tk.Label(display_frame, text="No medicines added.", font=("Arial", 12, "italic"), bg="#f0f0f0").pack()

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
    
    # Days selection (hidden initially)
    days_vars = {}
    day_frame = tk.Frame(add_window)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        days_vars[day] = tk.IntVar()
        tk.Checkbutton(day_frame, text=day, variable=days_vars[day]).pack(side=tk.LEFT)
    
    tk.Label(add_window, text="Dose:").pack()
    dose_var = ttk.Combobox(add_window, values=["1 pill", "2 pills", "3 pills"])
    dose_var.pack()
    dose_var.bind("<<ComboboxSelected>>", update_dose_times)
    
    # Time selection (initially hidden)
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

display_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
display_frame.pack(pady=20)

refresh_display()

tk.Button(root, text="Refresh", command=refresh_display, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Add Medicine", command=open_add_window, bg="#007BFF", fg="white").pack(pady=5)

root.mainloop()