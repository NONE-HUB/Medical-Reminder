import tkinter
from tkinter import ttk
from tkinter import messagebox
import tkinter.messagebox

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
            numcourses = numcourses_spinbox.get()
            numsemester = numsemester_spinbox.get()

            print("First name: " , firstname)
            print("Middle Name:" , middelname)
            print("Last name" , lastname)
            print("Title:" , title)
            print("Age:" , age)
            print("Nationality:" , nationality)
            print("# Courses:" , numcourses)
            print("# Semester:" , numsemester)
            print("Registration status:", registered_status)
            print("-------------------------------------------------------")
        
        else:
            tkinter.messagebox.showwarning(title="Error", message="First name and middle name and last name are required")
    
    else:
        tkinter.messagebox.showwarning(title="Error" , message="You have not accepted the terms")
    

    


window = tkinter.Tk()
window.title("Data entry form")

frame = tkinter.Frame(window)
frame.pack()

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

numcourses_label = tkinter.Label(courses_frame, text ="#Completed Courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0 , to='infinity')

numcourses_label.grid(row=0,column=1)
numcourses_spinbox.grid(row=1, column=1)


numsemester_label = tkinter.Label(courses_frame, text ="#Semester")
numsemester_spinbox = tkinter.Spinbox(courses_frame, from_=0 , to='infinity')

numsemester_label.grid(row=0,column=2)
numsemester_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10 ,pady=5)

#Accept terms
terms_frame = tkinter.LabelFrame(frame, text = "Terms and Condition")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10,)

accept_var = tkinter.StringVar(value="Not-Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text = "I accept the terms and condition", variable=accept_var, onvalue="Accepted", offvalue="Not-Accepted")
terms_check.grid(row=0, column=0)


#Button
button = tkinter.Button(frame, text = "Enter data", command=enter_data)
button.grid(row=3 , column=0, sticky="news", padx=20, pady=10)




window.mainloop()