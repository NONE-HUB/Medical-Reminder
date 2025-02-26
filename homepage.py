import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

# Database setup
def dataset_db():
    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            First_Name TEXT,
            Last_Name TEXT,
            Password TEXT
        )
    ''')
    conn.commit()
    conn.close()

dataset_db()  # Call the function to create the table

def register_client():
    email = entry_email.get()
    First_Name = entry_First_Name.get()
    Last_Name = entry_Last_Name.get()
    Password = entry_Password.get()

    if not (email and First_Name and Last_Name and Password):
        messagebox.showerror("Invalid", "Fill up all the fields.")
        return

    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO client (email, First_Name, Last_Name, Password) VALUES (?, ?, ?, ?)", (email, First_Name, Last_Name, Password))
        conn.commit()
        messagebox.showinfo("Success", "Successfully Registered!!")
        signup_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Sorry!", "This email is already registered")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        conn.close()

def login_client():
    email = login_email.get()
    password = login_Password.get()

    conn = sqlite3.connect("client.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE email=? AND Password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Congratulations", "Successfully logged in!")
    else:
        messagebox.showerror("Sorry!", "Username or Password Incorrect!")

def open_signup():
    global signup_window, entry_email, entry_First_Name, entry_Last_Name, entry_Password
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry('400x500')

    tk.Label(signup_window, text="Email").pack()
    entry_email = tk.Entry(signup_window)
    entry_email.pack()
    tk.Label(signup_window, text="First Name").pack()
    entry_First_Name = tk.Entry(signup_window)
    entry_First_Name.pack()
    tk.Label(signup_window, text="Last Name").pack()
    entry_Last_Name = tk.Entry(signup_window)
    entry_Last_Name.pack()
    tk.Label(signup_window, text="Password").pack()
    entry_Password = tk.Entry(signup_window, show="*")
    entry_Password.pack()
    tk.Button(signup_window, text='Next', command=register_client).pack()

root = tk.Tk()
root.title("Login Page")
root.geometry("800x600")

bg_image = Image.open(r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\bg.png")
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

bg_Label = tk.Label(root, image=bg_image)
bg_Label.place(relwidth=1, relheight=1)

tk.Label(root, text="Email").pack()
login_email = tk.Entry(root)
login_email.pack()

tk.Label(root, text="Password").pack()
login_Password = tk.Entry(root, show="*")
login_Password.pack()

tk.Button(root, text="Login", command=login_client).pack()
tk.Button(root, text="Sign Up", command=open_signup).pack()

root.mainloop()