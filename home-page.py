import tkinter
from tkinter import *
from tkinter import messagebox
<<<<<<< HEAD
from PIL import Image, ImageTk
=======
import json
import re
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk  
import os 
import openpyxl



root=Tk()
root.title("Image demo")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(400, 400)

user_db_file = "users.json"

PASSWORD_FILE = "password.json"

def load_users():
    try:
        with open(user_db_file , "r") as file:
            return json.load(file)
        
    except FileNotFoundError:
        return{}

def save_users(users):
    with open(user_db_file, "w") as file:
        json.dump(users , file)     

def get_stored_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            data = json.load(file)
            return data.get("password", None)  
    return None 

# Function to save password
def save_password(password):
    with open(PASSWORD_FILE, "w") as file:
        json.dump({"password": password}, file)

image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")

def signin_screen():

    root.withdraw()

    signin_screen = Toplevel(root)
    signin_screen.title("Welcome")
    signin_screen.geometry(f"{screen_width}x{screen_height}")
    signin_screen.minsize(400, 400) 

    image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
    bg_image=Label(signin_screen, image=image_path)
    bg_image.place(relheight=1,relwidth=1)

    frame = Frame(signin_screen, width =800 , height = 800 , bg = "white")
    frame.place(x=500, y=180)

    def enter_data():
        accepted = accept_var.get()

        if accepted=="Accepted":
            #user info
            firstname = first_name_entry.get()
            middelname = middle_name_entry.get()
            lastname = last_name_entry.get()
            
            if firstname and middelname and lastname:
                title = title_combobox.get()
                age = age_spinbox.get()
                nationality = nationality_combobox.get()

                #course info
                registered_status = reg_status_var.get()
                username = username_entry.get()
                password = current_password_entry.get()

                print("First name: " , firstname)
                print("Middle Name:" , middelname)
                print("Last name" , lastname)
                print("Title:" , title)
                print("Age:" , age)
                print("Nationality:" , nationality)
                print("username:" , username)
                print("password:" , password)
                print("Registration status:", registered_status)
                print("-------------------------------------------------------")
                messagebox.showinfo("Congratulatioons" , "Data has been entered")
                filepath = r"C:\Users\cis-c\OneDrive\Desktop\Medical-Reminder - Copy\data.xlsx"

                if not os.path.exists(filepath):
                    workbook = openpyxl.Workbook()
                    sheet = workbook.active
                    heading = ["First Name" , "Middle Name" , "Last Name" , "Title" , "Age" , "Nationality" , "#Courses" , "#Semester" , "Registration Status"]
                    sheet.append(heading)
                    workbook.save(filepath)
                workbook = openpyxl.load_workbook(filepath)
                sheet = workbook.active
                sheet.append([firstname , middelname , lastname , title , age , nationality , username , password , registered_status])
                workbook.save(filepath)

            else:
                tkinter.messagebox.showwarning(title="Error", message="First name and middle name and last name are required")
        
        else:
            tkinter.messagebox.showwarning(title="Error" , message="You have not accepted the terms")

    def register():
        username = username_entry.get()
        password = current_password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error" , "Username and password cannot be empty")
            return
        
        if len(username) <=8 or not username.isalnum():
            messagebox.showerror("Error" , "Username must be more that 8 alphanumeric characters and must contain one '_' character")
            return

        if username in users:
            messagebox.showerror("Error" , "Username already exists")
            return

        if username == password:
            messagebox.showerror("Error" , "Username and password cannot be same")
            return
        
        if len(password) <= 8 or not (re.search(r"[A-Z]",password) and re.search(r"[a-z]",password) and re.search(r"\d",password) and re.search(r"[!@#$%^&*]",password)):
            messagebox.showerror("Error", "Password must be 8 characters long and include:\n"
                                            "- At least 1 uppercase letter\n"
                                            "-Shouldn't contain any space\n"
                                            "- At least 1 lowercase letter\n"
                                            "- At least 1 digit\n"
                                            "- At least 1 special character (@, $, !, %, *, ?, &)")
            return

        users[username] = password
        save_users(users)
        messagebox.showinfo("Success" , "User registered successfully")

        register.mainloop()

    #saving user info
    user_info_frame = tkinter.LabelFrame(frame, text = "User Information")
    user_info_frame.grid(row=0 , column=0, padx=20, pady=10)

    first_name_label = tkinter.Label(user_info_frame, text ="First name")
    first_name_label.grid(row=0,column=0)

    middle_name_label = tkinter.Label(user_info_frame, text ="Middle name")
    middle_name_label.grid(row=0,column=1)

    last_name_label = tkinter.Label(user_info_frame, text = "Last name")
    last_name_label.grid(row=0,column=2)

    first_name_entry = tkinter.Entry(user_info_frame)
    middle_name_entry = tkinter.Entry(user_info_frame)
    last_name_entry = tkinter.Entry(user_info_frame)

    first_name_entry.grid(row=1,column=0)
    middle_name_entry.grid(row=1,column=1)
    last_name_entry.grid(row=1,column=2)

    title_label = tkinter.Label(user_info_frame, text="Title")
    title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
    title_label.grid(row=2,column=0)
    title_combobox.grid(row=3,column=0)

    age_label = tkinter.Label(user_info_frame, text="Age")
    age_spinbox = tkinter.Spinbox(user_info_frame, from_=18 , to =110)
    age_label.grid(row=2,column=2)
    age_spinbox.grid(row=3,column=1)

    nationality_label = tkinter.Label(user_info_frame, text ="Nationality")
    nationality_combobox = ttk.Combobox(user_info_frame, values=["Africa", "Antartica", "Asia", "Europe", "Australia", "North America", "South America"])

    nationality_label.grid(row=2,column=2)
    nationality_combobox.grid(row=3,column=2)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    #saving course info
    courses_frame = tkinter.LabelFrame(frame)
    courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    registered_label = tkinter.Label(courses_frame, text = "Regsitered form")

    reg_status_var = tkinter.StringVar(value="Not -Registered")
    registered_check = tkinter.Checkbutton(courses_frame, text = "Currently registered", variable=reg_status_var, onvalue="Registered" , offvalue= "Not-registered")

    registered_label.grid(row=0, column=0)
    registered_check.grid(row=1 ,column=0)

    username_label = tkinter.Label(courses_frame, text ="Username")
    username_entry = tkinter.Entry(courses_frame,text="username")

    username_label.grid(row=0,column=1)
    username_entry.grid(row=1, column=1)


    password_label = tkinter.Label(courses_frame, text ="Password")
    current_password_entry = tkinter.Entry(courses_frame, text = "password")

    password_label.grid(row=0,column=2)
    current_password_entry.grid(row=1, column=2)

    for widget in courses_frame.winfo_children():
        widget.grid_configure(padx=10 ,pady=5)

    #Accept terms
    terms_frame = tkinter.LabelFrame(frame, text = "Terms and Condition")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10,)

    accept_var = tkinter.StringVar(value="Not-Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text = "I accept the terms and condition", variable=accept_var, onvalue="Accepted", offvalue="Not-Accepted")
    terms_check.grid(row=0, column=0)

    def go_home():
        signin_screen.destroy()
        root.deiconify()

    #Button
    button = tkinter.Button(frame, text = "Enter data", command=enter_data)
    button.grid(row=3 , column=0, sticky="news", padx=20, pady=10)

    butoon_register = tkinter.Button(frame, text = "Register", command=register)
    butoon_register.grid(row=4,column=0, sticky="news",padx=20,pady=10)

    butoon_back = tkinter.Button(frame, text = "Back to Home Page", command=go_home)
    butoon_back.grid(row=5,column=0, sticky="news",padx=20,pady=10)

    signin_screen.mainloop()



def home_page():
    home_page = Toplevel(root)
    home_page.title("Welcome")
    home_page.geometry(f"{screen_width}x{screen_height}")
    home_page.minsize(400, 400) 

    image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
    bg_image=Label(home_page, image=image_path)
    bg_image.place(relheight=1,relwidth=1)

    frame = Frame(home_page, width =800 , height = 500 , bg = "white")
    frame.place(x=370, y=180)

    def home():
        home = Toplevel(root)
        home.title("Welcome")
        home.geometry(f"{screen_width}x{screen_height}")
        home.minsize(400, 400) 

        image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
        bg_image=Label(home, image=image_path)
        bg_image.place(relheight=1,relwidth=1)

        frame = Frame(home, width =800 , height = 500 , bg = "white")
        frame.place(x=370, y=180)

        home.mainloop()

    def reminder():
        reminder = Toplevel(root)
        reminder.title("Welcome")
        reminder.geometry(f"{screen_width}x{screen_height}")
        reminder.minsize(400, 400) 

        image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
        bg_image=Label(reminder, image=image_path)
        bg_image.place(relheight=1,relwidth=1)

        frame = Frame(reminder, width =800 , height = 800 , bg = "white",pady=50,padx=150)
        frame.place(x=475, y=100)

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

        def update_days_visibility(event):
            if frequency_var.get() == "Selected Days":
                day_frame.pack()
            else:
                day_frame.pack_forget()

        def update_dose_times(event):
            selected_dose = int(dose_var.get()[0])
            for i in range(3):
                if i < selected_dose:
                    time_labels[i].pack()
                    time_vars[i].pack()
                else:
                    time_labels[i].pack_forget()
                    time_vars[i].pack_forget()

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

            messagebox.showinfo("Success", "Medicine added successfully!")

            add_window.destroy()

            refresh_display()

        def refresh_display():
            for widget in frame.winfo_children():
                widget.destroy()
            
            today = datetime.today().strftime('%A, %B %d, %Y')
            tk.Label(frame, text=today, font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
            
            medicines = get_medicines()
            if medicines:
                for med in medicines:
                    med_id, name, dose, frequency, days, times, status = med
                    tk.Label(frame, text=f"Medicine: {name}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack()
                    tk.Label(frame, text=f"Dose: {dose}", font=("Arial", 10), bg="#f0f0f0").pack()
                    
                    times_list = times.split(",")
                    for i, time in enumerate(times_list):
                        formatted_time = format_time(time.strip())
                        tk.Label(frame, text=f"{i+1}st Dose: {formatted_time}", font=("Arial", 10), bg="#f0f0f0").pack()
                    
                    tk.Label(frame, text="-----------------------------", bg="#f0f0f0").pack()
            else:
                tk.Label(frame, text="No medicines added.", font=("Arial", 12, "italic"), bg="#f0f0f0").pack()

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

        tk.Label(frame, text="Medicine Reminder", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)


        refresh_display()

        tk.Button(frame, text="Refresh", command=refresh_display, fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",15) , justify="center").pack(pady=10)
        tk.Button(frame, text="Add Medicine", command=open_add_window, fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",) , justify="center").pack(pady=5)

        reminder.mainloop()

    def history():
        history = Toplevel(root)
        history.title("Welcome")
        history.geometry(f"{screen_width}x{screen_height}")
        history.minsize(400, 400) 

        image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
        bg_image=Label(history, image=image_path)
        bg_image.place(relheight=1,relwidth=1)

        frame = Frame(history, width =800 , height = 500 , bg = "white")
        frame.place(x=370, y=180)

        def change_password():
            global USER_PASSWORD
            current = current_password_entry.get()
            new = new_password_entry.get()
            confirm = confirm_password_entry.get()

            if current != USER_PASSWORD:
                messagebox.showerror("Error", "Current password is incorrect!")
                return

            if new == "":
                messagebox.showerror("Error", "New password cannot be empty!")
                return

            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match!")
                return

            # Update password in file
            save_password(new)
            USER_PASSWORD = new  # Update global variable
            messagebox.showinfo("Success", "Password changed successfully!")
            history.destroy()  # Close window after changing password

        USER_PASSWORD = get_stored_password()

        tk.Label(frame, text="Current Password:").pack()
        current_password_entry = tk.Entry(frame)
        current_password_entry.pack()

        tk.Label(frame, text="New Password:").pack()
        new_password_entry = tk.Entry(frame)
        new_password_entry.pack()

        tk.Label(frame, text="Confirm New Password:").pack()
        confirm_password_entry = tk.Entry(frame)
        confirm_password_entry.pack()

        tk.Button(frame, text="Change Password", command=change_password).pack()

        history.mainloop()

    def setting():
        setting = Toplevel(root)
        setting.title("Welcome")
        setting.geometry(f"{screen_width}x{screen_height}")
        setting.minsize(400, 400) 

        image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
        bg_image=Label(setting, image=image_path)
        bg_image.place(relheight=1,relwidth=1)

        frame = Frame(setting, width =800 , height = 500 , bg = "white")
        frame.place(x=370, y=180)

        setting.mainloop()

    home_entry = Button(frame, width=7 ,text="Home", fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center",command=home)
    home_entry.place(x=20 , y = 180)
    Frame(frame, width=3,height=180,bg="black").place(x=97,y=0)

    reminder_entry = Button(frame, width=9 ,text="Reminder", fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center",command=reminder)
    reminder_entry.place(x=190 , y = 320)
    Frame(frame, width=3,height=320,bg="black").place(x=277,y=0)

    history_entry = Button(frame, text="History",  width=7,  fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center", command=history)
    history_entry.place(x=400 , y = 180)
    Frame(frame, width=3,height=180,bg="black").place(x=470,y=0)

    setting_entry = Button(frame,text="Setting" , width=7 , fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center",command=setting)
    setting_entry.place(x=620 , y = 320)
    Frame(frame, width=3,height=320,bg="black").place(x=690,y=0)

    home_page.mainloop()

def signin():
    username = username_entry.get()
    password = current_password_entry.get()

    if users.get(username) == password:
        home_page()

    else:
        messagebox.showerror("Invalid","Invalid username and password")

users = load_users()

bg_image=Label(root, image=image_path)
bg_image.place(relheight=1,relwidth=1)

frame = Frame(root, width =800 , height = 500 , bg = "white")
frame.place(x=370, y=180)

sign_in_label = Label(frame, text="Sign in", fg = "#57a1f8" , bg = "white" , font = ("Microsoft YaHei UI Light",80,"bold"))
sign_in_label.place(x = 220 , y = 20)

def on_enter(e):
    username_entry.delete(0, 'end')

def on_leave(e):
    name=username_entry.get()
    if name == "":
        username_entry.insert(0,'Username')


username_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
username_entry.place(x=200 , y = 187)
username_entry.insert(0, "Username")
username_entry.bind('<FocusIn>', on_enter)
username_entry.bind('<FocusOut>',on_leave)
Frame(frame, width=400,height=2,bg="black").place(x=200,y=230)

def on_enter(e):
    current_password_entry.delete(0, 'end')

def on_leave(e):
    name=current_password_entry.get()
    if name == "":
        current_password_entry.insert(0,'Password')


current_password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
current_password_entry.place(x=200 , y = 305)
current_password_entry.insert(0, "Password")
current_password_entry.bind('<FocusIn>', on_enter)
current_password_entry.bind('<FocusOut>', on_leave)
Frame(frame, width=400,height=2,bg="black").place(x=200,y=348)
print(username_entry.get())
print(current_password_entry.get())

USER_PASSWORD = current_password_entry.get()

forgot_label = Label(frame, text="Forgot Password ?", fg="black",border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",10) )
forgot_label.place(x=500, y = 353 )

signin_button = Button(frame, text="Sign in", width=80 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0 , command= signin )
signin_button.place(x=110 , y = 400)

no_acc_label = tkinter.Label(frame, text="Don't have an account?" , fg = "black" , bg = "white" , font = ("Microsoft YaHei UI Light", 9))
no_acc_label.place(x = 305 , y = 456)

sign_up_label = Button(frame , text = "Sign up"  , width=6 ,  border =0 , bg = "white" , cursor = "hand2" , fg = "#57a1f8",command=signin_screen)
sign_up_label.place(x = 445 , y = 456)


root.mainloop()