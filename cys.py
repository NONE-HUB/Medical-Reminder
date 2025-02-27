import sqlite3
from tkinter import messagebox, Toplevel, Label, Entry, Button, ttk, Frame, IntVar, Checkbutton

# Function to delete medicine
def delete_medicine(med_id):
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Medicine deleted successfully!")
    refresh_display()

# Function to open the edit window
def open_edit_window(med):
    global edit_window, edit_name_entry, edit_dose_var, edit_frequency_var, edit_days_vars, edit_time_vars, edit_time_labels, edit_day_frame
    
    # Open a new top-level window for editing
    edit_window = Toplevel(root)
    edit_window.title("Edit Medicine")
    edit_window.geometry("400x500")
    
    med_id, name, dose, frequency, days, times, status = med
    
    # Name field
    Label(edit_window, text="Medicine Name:").pack()
    edit_name_entry = Entry(edit_window)
    edit_name_entry.insert(0, name)
    edit_name_entry.pack()

    # Frequency selection
    Label(edit_window, text="Frequency:").pack()
    edit_frequency_var = ttk.Combobox(edit_window, values=["Daily", "Selected Days"])
    edit_frequency_var.set(frequency)
    edit_frequency_var.pack()

    # Days checkboxes for "Selected Days" frequency
    edit_days_vars = {}
    edit_day_frame = Frame(edit_window)
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        edit_days_vars[day] = IntVar()
        if days and day in days.split(","):
            edit_days_vars[day].set(1)
        Checkbutton(edit_day_frame, text=day, variable=edit_days_vars[day]).pack(side="left")
    
    if frequency == "Selected Days":
        edit_day_frame.pack()

    # Dose selection
    Label(edit_window, text="Dose:").pack()
    edit_dose_var = ttk.Combobox(edit_window, values=["1 pill", "2 pills", "3 pills"])
    edit_dose_var.set(dose)
    edit_dose_var.pack()

    # Time selection for each dose
    edit_time_vars = []
    edit_time_labels = []
    times_list = times.split(",")
    for i in range(3):
        edit_time_labels.append(Label(edit_window, text=f"Dose {i+1} Time:"))
        edit_time_vars.append(ttk.Combobox(edit_window, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)]))
        if i < len(times_list):
            edit_time_vars[i].set(times_list[i])
        edit_time_labels[i].pack()
        edit_time_vars[i].pack()

    # Save button to update medicine details
    Button(edit_window, text="Save", command=lambda: save_edited_medicine(med_id), bg="green", fg="white").pack(pady=10)

    # Cancel button to close the edit window
    Button(edit_window, text="Cancel", command=edit_window.destroy, bg="red", fg="white").pack()

# Function to save the edited medicine details
def save_edited_medicine(med_id):
    name = edit_name_entry.get()
    dose = edit_dose_var.get()
    frequency = edit_frequency_var.get()
    days = ",".join([day for day, var in edit_days_vars.items() if var.get()]) if frequency == "Selected Days" else ""
    selected_dose = int(dose[0])  # Extract the number of pills (e.g., "1 pill" -> 1)
    times = ",".join([edit_time_vars[i].get() for i in range(selected_dose)])

    # Validate fields before saving
    if not (name and dose and frequency and times):
        messagebox.showerror("Error", "Please fill all fields.")
        return

    # Update the database with the new details
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE medicines SET name=?, dose=?, frequency=?, days=?, times=? WHERE id=?",
                   (name, dose, frequency, days, times, med_id))
    conn.commit()
    conn.close()

    # Success message
    messagebox.showinfo("Success", "Medicine updated successfully!")

    # Close the edit window and refresh the display
    edit_window.destroy()
    refresh_display()

# Function to refresh the display
def refresh_display():
    for widget in display_frame.winfo_children():
        widget.destroy()

    # Fetch updated medicines from the database
    medicines = get_medicines()
    if medicines:
        for med in medicines:
            med_id, name, dose, frequency, days, times, status = med
            Label(display_frame, text=f"Medicine: {name}").pack()
            Label(display_frame, text=f"Dose: {dose}").pack()

            times_list = times.split(",")
            for i, time in enumerate(times_list):
                formatted_time = format_time(time.strip())
                Label(display_frame, text=f"{i+1}st Dose: {formatted_time}").pack()

            button_frame = Frame(display_frame)
            button_frame.pack()

            # Edit and Delete buttons
            Button(button_frame, text="Delete", command=lambda med_id=med_id: delete_medicine(med_id), bg="red", fg="white").pack(side="left", padx=5)
            Button(button_frame, text="Edit", command=lambda med_id=med_id: open_edit_window(med), bg="blue", fg="white").pack(side="left", padx=5)

# Function to fetch medicines from the database
def get_medicines():
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()
    conn.close()
    return data

# Format time for display (you can customize this function)
def format_time(time):
    return time  # Placeholder for formatting logic if needed

# UI Setup for Testing (This part would be integrated into your existing app)
from tkinter import Tk, Button, Frame

root = Tk()
root.title("Medicine Reminder App")

# Display frame for the medicines
display_frame = Frame(root)
display_frame.pack(pady=20)

# Refresh the display initially
refresh_display()

root.mainloop()
