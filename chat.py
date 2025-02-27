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

root=Tk()
root.title("Image demo")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(400, 400)

user_db_file = "users.json"

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
    try:
        with open("password.txt", "r") as file:
            password = file.read().strip()
            return password
    except FileNotFoundError:
            return ""  

image_path=PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\medicine reminder\medicine_reminder\background_image.png")

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
            
            firstname = first_name_entry.get()
            middelname = middle_name_entry.get()
            lastname = last_name_entry.get()
            
            if firstname and middelname and lastname:
                title = title_combobox.get()
                age = age_spinbox.get()
                nationality = nationality_combobox.get()

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

    terms_frame = tkinter.LabelFrame(frame, text = "Terms and Condition")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10,)

    accept_var = tkinter.StringVar(value="Not-Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text = "I accept the terms and condition", variable=accept_var, onvalue="Accepted", offvalue="Not-Accepted")
    terms_check.grid(row=0, column=0)

    def go_home():
        signin_screen.destroy()
        root.deiconify()

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

    
    global global_username, global_password
    global_username = username_entry.get()
    global_password = current_password_entry.get()
    print(f"Username: {global_username}")
    print(f"Password: {global_password}")

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

        def get_medicines():
            conn = sqlite3.connect("medicine.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicines")
            data = cursor.fetchall()
            conn.close()
            return data

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

            if len(get_medicines()) >= 5:
                messagebox.showerror("Error", "Only 5 medicines can be added!")
                return
            

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
           
            refresh_display()

            add_window.destroy()

        def delete_medicine(med_id):
            conn = sqlite3.connect("medicine.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicines WHERE id=?", (med_id,))
            conn.commit()
            conn.close()
            refresh_display()

        def edit_medicine(med_id):

            conn = sqlite3.connect("medicine.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicines WHERE id=?", (med_id,))
            med = cursor.fetchone()
            conn.close()

            open_edit_window(med)

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
            edit_window.destroy()
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
                    
                    button_frame = tk.Frame(frame, bg="#f0f0f0")
                    button_frame.pack()
                    tk.Button(button_frame, text="Delete", command=lambda med_id=med_id: delete_medicine(med_id), bg="red", fg="white").pack(side=tk.LEFT, padx=5)
                    tk.Button(button_frame, text="Edit", command=lambda med_id=med_id: edit_medicine(med_id), bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
            

                    tk.Label(frame, text="-----------------------------", bg="#f0f0f0").pack()
            else:
                tk.Label(frame, text="No medicines added.", font=("Arial", 12, "italic"), bg="#f0f0f0").pack()

        def open_add_window():
            global add_window, name_entry, dose_var, frequency_var, days_vars, time_vars, time_labels, day_frame
            
            add_window = tk.Toplevel(root)
            add_window.title("Add Medicine")
            add_window.geometry("600x600")
            
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

        tk.Button(reminder, text="Refresh", command=refresh_display, fg="black" , border=0,  bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",15) , justify="center").place(x=650,y=50)
        tk.Button(reminder, text="Add Medicine", command=open_add_window, fg="black" , border=0,  bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",) , justify="center").place(x=750,y=50)

        reminder.mainloop()

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

        def change_page():
            change_page = Toplevel(root)
            change_page.title("Welcome")
            change_page.geometry(f"{screen_width}x{screen_height}")
            change_page.minsize(400, 400) 

            image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
            bg_image=Label(change_page, image=image_path)
            bg_image.place(relheight=1,relwidth=1)

            frame = Frame(change_page, width =800 , height = 500 , bg = "white")
            frame.place(x=370, y=180)

            def change_password():
                current_password = current_password_entry.get()
                new_password = new_password_entry.get()
                confirm_password = confirm_password_entry.get()

                print(f"Current password: {current_password}")
                print(f"New password: {new_password}")
                print(f"Confirm password: {confirm_password}")

                if new_password == "":
                        messagebox.showerror("Error", "New password cannot be empty!")
                        return

                if new_password != confirm_password:
                        messagebox.showerror("Error", "New passwords do not match!")
                        return

                def save_password(new_password):

                    with open("password.txt", "w") as file:
                            file.write(new_password)

                def get_stored_password():
                            try:
                                with open("password.txt", "r") as file:
                                    return file.read().strip()
                            except FileNotFoundError:
                                return ""  
                            
                save_password(new_password)
                messagebox.showinfo("Success", "Password changed successfully!")

                def on_enter(e):
                        current_password_entry.delete(0, 'end')

                def on_leave(e):
                        name=current_password_entry.get()
                        if name == "":
                            current_password_entry.insert(0,'Current Password')

            change_in_label = Label(frame, text="Change Your Password", fg = "#57a1f8" , bg = "white" , font = ("Microsoft YaHei UI Light",40,"bold"))
            change_in_label.place(x = 100 , y = 20)

            def on_enter(e):
                        current_password_entry.delete(0, 'end')

            def on_leave(e):
                        name=current_password_entry.get()
                        if name == "":
                            current_password_entry.insert(0,'New Psssword')

            current_password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
            current_password_entry.place(x=200 , y = 187)
            current_password_entry.insert(0, "Current Password")
            current_password_entry.bind('<FocusIn>', on_enter)
            current_password_entry.bind('<FocusOut>',on_leave)
            Frame(frame, width=400,height=2,bg="black").place(x=200,y=230)

            def on_enter(e):
                        new_password_entry.delete(0, 'end')

            def on_leave(e):
                        name=new_password_entry.get()
                        if name == "":
                            new_password_entry.insert(0,'New Psssword')

            new_password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
            new_password_entry.place(x=200 , y = 267)
            new_password_entry.insert(0, "New Password")
            new_password_entry.bind('<FocusIn>', on_enter)
            new_password_entry.bind('<FocusOut>',on_leave)
            Frame(frame, width=400,height=2,bg="black").place(x=200,y=310)

            def on_enter(e):
                            confirm_password_entry.delete(0, 'end')

            def on_leave(e):
                            name=confirm_password_entry.get()
                            if name == "":
                                confirm_password_entry.insert(0,'Confirm Password')

            confirm_password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
            confirm_password_entry.place(x=200 , y = 347)
            confirm_password_entry.insert(0, "Confirm your Password")
            confirm_password_entry.bind('<FocusIn>', on_enter)
            confirm_password_entry.bind('<FocusOut>',on_leave)
            Frame(frame, width=400,height=2,bg="black").place(x=200,y=390)

            change_button = Button(frame, text="Change Password", width=80 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0 , command= change_password )
            change_button.place(x=110 , y = 420)

        def go_home():
            setting.destroy()
            root.deiconify()

        change_pass_entry = Button(frame, text="Change your password", width=80 , height=3 , pady=7, bg="#57a1f8", fg = "white" , border=0  ,command= change_page )
        change_pass_entry.place(x=110 , y = 100)

        log_entry = Button(frame, text="Log out", width=80 , height=3 , pady=7, bg="#57a1f8", fg = "white" , border=0  ,command= go_home )
        log_entry.place(x=110 , y = 240)

        setting.mainloop()

    reminder_entry = Button(frame, text="Reminder", width=80 , height=3 , pady=7, bg="#57a1f8", fg = "white" , border=0  ,command= reminder )
    reminder_entry.place(x=110 , y = 100)


    setting_entry = Button(frame,text="Setting" , width=80 ,height=3, pady=7, bg="#57a1f8", fg = "white" , border=0 ,command=setting)
    setting_entry.place(x=110 , y = 240)

    home_page.mainloop()

def signin():
    username = username_entry.get()
    entered_password = current_password_entry.get()
    stored_password = get_stored_password()

    if users.get(username) and entered_password == get_stored_password():
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