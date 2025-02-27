import tkinter
from tkinter import *
from tkinter import messagebox
import json
import re
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import os
import openpyxl

# Initialize main window
root = Tk()
root.title("Medicine Reminder")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(400, 400)

# Load background image
try:
    image_path = PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\background_image.png")
    bg_image = Label(root, image=image_path)
    bg_image.place(relheight=1, relwidth=1)
except Exception as e:
    print(f"Error loading image: {e}")
    bg_image = Label(root, text="Background Image Not Found", bg="white")
    bg_image.place(relheight=1, relwidth=1)

# Main menu frame
frame = Frame(root, width=800, height=500, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Function to open the reminder window
def reminder():
    reminder_window = Toplevel(root)
    reminder_window.title("Reminder")
    reminder_window.geometry(f"{screen_width}x{screen_height}")
    reminder_window.minsize(400, 400)

    try:
        reminder_image_path = PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\background_image.png")
        reminder_bg_image = Label(reminder_window, image=reminder_image_path)
        reminder_bg_image.place(relheight=1, relwidth=1)
    except Exception as e:
        print(f"Error loading image: {e}")
        reminder_bg_image = Label(reminder_window, text="Background Image Not Found", bg="white")
        reminder_bg_image.place(relheight=1, relwidth=1)

    reminder_frame = Frame(reminder_window, width=800, height=800, bg="white", pady=50, padx=150)
    reminder_frame.place(relx=0.5, rely=0.5, anchor="center")

# Function to open the settings window
def setting():
    setting_window = Toplevel(root)
    setting_window.title("Settings")
    setting_window.geometry(f"{screen_width}x{screen_height}")
    setting_window.minsize(400, 400)

    try:
        setting_image_path = PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\background_image.png")
        setting_bg_image = Label(setting_window, image=setting_image_path)
        setting_bg_image.place(relheight=1, relwidth=1)
    except Exception as e:
        print(f"Error loading image: {e}")
        setting_bg_image = Label(setting_window, text="Background Image Not Found", bg="white")
        setting_bg_image.place(relheight=1, relwidth=1)

    setting_frame = Frame(setting_window, width=800, height=500, bg="white")
    setting_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add widgets to the settings window
    change_pass_entry = Button(setting_frame, text="Change your password", width=20, height=2, bg="#57a1f8", fg="white", border=0, command=change_password_window)
    change_pass_entry.pack(pady=10)

    log_entry = Button(setting_frame, text="Log out", width=20, height=2, bg="#57a1f8", fg="white", border=0, command=setting_window.destroy)
    log_entry.pack(pady=10)

# Function to open the change password window
def change_password_window():
    change_window = Toplevel(root)
    change_window.title("Change Password")
    change_window.geometry(f"{screen_width}x{screen_height}")
    change_window.minsize(400, 400)

    try:
        change_image_path = PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\background_image.png")
        change_bg_image = Label(change_window, image=change_image_path)
        change_bg_image.place(relheight=1, relwidth=1)
    except Exception as e:
        print(f"Error loading image: {e}")
        change_bg_image = Label(change_window, text="Background Image Not Found", bg="white")
        change_bg_image.place(relheight=1, relwidth=1)

    change_frame = Frame(change_window, width=800, height=500, bg="white")
    change_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Function to handle password change
    def change_password():
        current_password = current_password_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validate inputs
        if new_password == "":
            messagebox.showerror("Error", "New password cannot be empty!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        # Save the new password
        with open("password.txt", "w") as file:
            file.write(new_password)

        messagebox.showinfo("Success", "Password changed successfully!")
        change_window.destroy()

    # Add widgets to the change password window
    current_password_entry = Entry(change_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 22))
    current_password_entry.insert(0, "Current Password")
    current_password_entry.bind('<FocusIn>', lambda e: current_password_entry.delete(0, 'end'))
    current_password_entry.bind('<FocusOut>', lambda e: current_password_entry.insert(0, 'Current Password') if current_password_entry.get() == "" else None)
    current_password_entry.pack(pady=10)

    new_password_entry = Entry(change_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 22))
    new_password_entry.insert(0, "New Password")
    new_password_entry.bind('<FocusIn>', lambda e: new_password_entry.delete(0, 'end'))
    new_password_entry.bind('<FocusOut>', lambda e: new_password_entry.insert(0, 'New Password') if new_password_entry.get() == "" else None)
    new_password_entry.pack(pady=10)

    confirm_password_entry = Entry(change_frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 22))
    confirm_password_entry.insert(0, "Confirm Password")
    confirm_password_entry.bind('<FocusIn>', lambda e: confirm_password_entry.delete(0, 'end'))
    confirm_password_entry.bind('<FocusOut>', lambda e: confirm_password_entry.insert(0, 'Confirm Password') if confirm_password_entry.get() == "" else None)
    confirm_password_entry.pack(pady=10)

    change_button = Button(change_frame, text="Change Password", width=20, height=2, bg="#57a1f8", fg="white", border=0, command=change_password)
    change_button.pack(pady=10)

# Add buttons to the main menu
reminder_entry = Button(frame, text="Reminder", width=20, height=2, bg="#57a1f8", fg="white", border=0, command=reminder)
reminder_entry.pack(pady=10)

setting_entry = Button(frame, text="Settings", width=20, height=2, bg="#57a1f8", fg="white", border=0, command=setting)
setting_entry.pack(pady=10)

# Start the main loop
root.mainloop()