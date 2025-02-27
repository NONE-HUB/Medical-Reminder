import sqlite3
import time
from plyer import notification
from tkinter import messagebox, Toplevel, Label, Entry, Button, ttk, Frame, IntVar, Checkbutton

# Function to send notification
def send_notification(medicine_name, dose_time):
    notification.notify(
        title=f"Time to take {medicine_name}",
        message=f"Don't forget to take your {medicine_name} at {dose_time}.",
        timeout=10  # Duration in seconds for how long the notification will stay
    )

# Function to check if it's time to send notifications
def check_notifications():
    # Get the current time (just hour:minute)
    current_time = time.strftime("%H:%M")

    # Fetch medicines from the database
    medicines = get_medicines()

    # Iterate through each medicine and check if any medicine's time matches the current time
    for med in medicines:
        med_id, name, dose, frequency, days, times, status = med
        times_list = times.split(",")  # Multiple times if the medicine is taken more than once

        for dose_time in times_list:
            formatted_time = format_time(dose_time.strip())
            
            # If current time matches the dose time, send a notification
            if formatted_time == current_time:
                send_notification(name, formatted_time)

    # Repeat checking every 60 seconds
    root.after(60000, check_notifications)

# Function to fetch medicines from the database
def get_medicines():
    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()
    conn.close()
    return data

# Format time for display (you can customize this function)
def format_time(time_str):
    return time_str.strip()  # Assuming time in 24-hour format (e.g., "08:00")

# UI Setup for Testing (This part would be integrated into your existing app)
from tkinter import Tk, Button, Frame

root = Tk()
root.title("Medicine Reminder App")

# Add a simple button to start notifications check
Button(root, text="Start Notifications", command=check_notifications).pack(pady=20)

root.mainloop()
