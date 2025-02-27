import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime, timedelta
from plyer import notification 
import threading


root=tk.Tk()
root.title("Medicine_Reminmder")
root.geometry("600x700")
root.configure(bg="#f0f0f0")
edit_dose_var=tk.StringVar
edit_regularity_var=tk.StringVar
edit_time_vars=tk.StringVar
def inaugurate_db():
    conn= sqlite3.connect("medication.db")
    cursor=conn.cursor()
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS medication(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     dose TEXT,
     regularity TEXT,
     days TEXT,
     times TEXT,
     status TEXT DEFAULT 'Pending')


''')
    
    conn.commit()
    conn.close()

inaugurate_db()

def get_medication():
    conn=sqlite3.connect("medication.db")
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM medication")
    data=cursor.fetchall()
    conn.close()
    return data

def format_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
    except ValueError:
        return time_str
    
def update_days_visibility(event):
    if regularity_var.get()=='Selective days':
        day_frame.pack()

    else:
        day_frame.pack_forget()

def update_dose_time(event):
    global time_vars
    selected_dose= int(dose_var.get()[0])
    for i in range(3):
        if i<selected_dose:
            time_labels[i].pack()
            time_vars[i].pack()

        else:
            time_labels[i].pack_forget()
            time_vars[i].pack_forget()

            

def add_medication():
    if len (get_medication())>=5:
        messagebox.showerror("Error","You can add only 5 medicines.")
        return
    
    name= name_entry.get()
    dose=dose_var.get()
    regularity=regularity_var.get()
    days=",". join([day for day, var in days_vars.items()if var.get()]) if regularity=="Selective days" else""
    selected_dose= int(dose[0])
    times= ",".join([time_vars[i].get()for i in range(selected_dose)])

    if not (name and dose and regularity and times):
        messagebox.showerror("Error", "All the field must be included!")
        return
    
    conn=sqlite3.connect("medication.db")
    cursor=conn.cursor()
    cursor.execute ("INSERT INTO medication (name, dose, regularity, days, times) VALUES(?,?,?,?,?)",
                    (name, dose,regularity,days,times))

    conn.commit()
    conn.close()

    messagebox.showinfo("Successful","Medicine updated!!")
    add_window.destroy()
    refresh_display()

def remove_medication(med_id):
    conn=sqlite3.connect("medication.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM medication WHERE id=?",(med_id,))
    conn.commit()
    conn.close()
    refresh_display()


def edit_medication(med_id):
    conn=sqlite3.connect("medication.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM medication  WHERE id=?",(med_id,))
    med=cursor.fetchone()
    conn.close()
    open_edit_window(med)


def open_edit_window(med):
    global edit_window, edit_name_entry, edit_dose_var, edit_regularity_var, edit_days_vars, edit_time_vars, edit_time_labels, edit_day_frame

    edit_window=tk.Toplevel(root)
    edit_window.title("Edit Medication")
    edit_window.geometry("400x500")

    med_id, name, dose, regularity,days, times, status= med
    tk.Label(edit_window, text="Medication Name:").pack()
    edit_name_entry=tk.Entry(edit_window)
    edit_name_entry.insert(0, name)
    edit_name_entry.pack()
   
    tk.Label(edit_window, text="Regularity:").pack()
    edit_regularity_var= ttk.Combobox(edit_window, values=["Daily", "Selective days"])
    edit_regularity_var.set(regularity)
    edit_regularity_var.pack()
    edit_regularity_var.bind("<<ComboboxSelected>>", update_days_visibility)

    edit_days_vars={}
    edit_day_frame= tk.Frame(edit_window)
    for day in["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        edit_days_vars[day]=tk.IntVar()#AAAAA
        if days and day in days.split(","):
            edit_days_vars[day].set(1)
            tk.Checkbutton (edit_day_frame, text=day, variable=edit_days_vars[day]).pack(side=tk.LEFT)

    if regularity=="Selective days":
        edit_day_frame.pack()

        tk.Label(edit_window, text="Dose:").pack()
        edit_dosage_var=ttk.Combobox(edit_window, values=["1 pill","2 pills","3 pills"])
        edit_dosage_var.set(dose)
        edit_dosage_var.pack()
        edit_dosage_var.bind("<<ComboboxSelected>>", update_dose_time)

        edit_time_vars=[]
        edit_time_labels=[]
        times_list=times.split(",")
        for i in range(3):
            edit_time_labels.append(tk.Label(edit_window, text=f"Dose{i+1} Time:"))
            edit_time_vars.append(ttk.Combobox(edit_window, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60, 15)]))
            if i <len(times_list):
                edit_time_vars[i].set(times_list[i])
            edit_time_labels[i].pack()
            edit_time_vars[i].pack()

        tk.Button(edit_window, text="Ok", command=lambda:saving_edited_medication(med_id), bg="#008000", fg="#FFFFFF").pack(pady=10)
        tk.Button(edit_window, text="Quit", command=edit_window.destroy, bg="#FF0000", fg="FFFFFF") .pack()


def saving_edited_medication(med_id):
    name=edit_name_entry.get()
    dose= edit_dose_var.get()
    regularity=edit_regularity_var.get()
    days=",".join([day for day, var in edit_days_vars.items()if var.get()]) if regularity=="Selective days" else""
    selected_dose=int(dose[0])
    times=",".join([edit_time_vars[i].get() for i in range(selected_dose)]) 
   
    if not(name and dose and regularity and times):
        messagebox.showerror("Error","All details must be included! ")
        return
    conn=sqlite3.connect("medication.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE medication SET name=?, dosage=?, regularity=?, days=?, times=? WHERE id=?", 
                   (name, dose,regularity,days, times, med_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Successful!!","Updated successfullu!!")
    edit_window.destroy()
    refresh_display()


def refresh_display():
    for widget in display_frame.winfo_children():
        widget.destroy()

    today=datetime.today().strftime('%A,%B,%d,%Y')
    tk.Label(display_frame, text=today,font=("Times New Roman",14,'bold'), bg="#f0f0f0").pack(pady=10)
    medicines= get_medication()
    if medicines:
        for med in medicines:
            med_id, name,dosage,regularity,days,times, status=med
            tk.Label(display_frame, text=f"Medication:{name}", font=("Times New Roman", 12,'bold'),bg="#f0f0f0").pack()
            tk.Label(display_frame, text=f"Dosage:{dosage}", font=("Times New Roman",11), bg="#f0f0f0").pack()
            
            times_list=times.split(",")
            for i, time in enumerate(times_list):
                formatted_time=format_time(time.strip())
                tk.Label(display_frame, text=f"{i+1}st pill:{formatted_time}",font=("Times New Roman",11),bg="#f0f0f0").pack()

            button_frame=tk.Frame(display_frame, bg="#f0f0f0")
            button_frame.pack()
            tk.Button(button_frame, text="Remove", command= lambda med_id=med_id:remove_medication(med_id),bg="#FF0000", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Edit", command=lambda med_id=med_id:edit_medication(med_id),bg="#0000FF", fg="#FFFFFF").pack(side=tk.LEFT, padx=5)
            tk.Label(display_frame, text="---------------------------",bg="#f0f0f0").pack()
    else:
        tk.Label(display_frame, text="Medicines Not Added!!", font=("Times New Roman",11,"bold"), bg="#f0f0f0").pack()
edit_dose_var=tk.StringVar()
edit_regularity_var=tk.StringVar()

def open_add_window():
    global add_window, name_entry, dose_var, regularity_var, days_vars, times_vars, time_labels, day_frame

    add_window=tk.Toplevel(root)
    add_window.title("Add Medication")
    add_window.geometry("400x500")

    tk.Label(add_window, text="Medication Name:").pack()
    medicine_name_entry=tk.Entry(add_window)
    medicine_name_entry.pack()

    tk.Label(add_window, text="Medicine name:").pack()
    name_entry=tk.Entry(add_window)
    name_entry.pack()
    tk.Label(add_window, text="Regularity:").pack()
    regularity_var=ttk.Combobox(add_window, values=["Daily","Selective days"])
    regularity_var.pack()
    regularity_var.bind("<<ComboboxSelected>>", update_days_visibility)

    days_vars={}
    day_frame=tk.Frame(add_window)
    for day in["Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        days_vars[day]=tk.IntVar()
        tk.Checkbutton(day_frame, text= day, variable=days_vars[day]).pack()
    
    tk.Label(add_window, text="Dose:").pack()
    dosage_var=ttk.Combobox(add_window, values=["1 pill","2 pills","3 pills"])
    dosage_var.pack()
    dosage_var.bind("<<ComboboxSelected>>", update_dose_time)

    time_vars=[]

    time_labels=[]
    for i in range(3):
        time_labels.append(tk.Label(add_window, text=f"Dose{i+1}Time:"))
        time_vars.append(ttk.Combobox(add_window, values=[f"{h:02d}:{m:02d}" for h in range(24) for m in range(0,60,15)]))
    tk.Button(add_window, text= "Next", command=add_medication, bg="#008000", fg="#FFFFFF").pack(pady=10)
    tk.Button(add_window, text="Quit", command=add_window.destroy, bg=" #FF0000", fg="#FFFFFF").pack() 


def check_notification():
 medicines=get_medication() 
 now=datetime.now().strftime("%H:%M")
 for med in medicines:     
    times_list=med[5].split(",")
    for time in times_list:
 
        if time.strip()==now:
           notification.notify(
              title="Medicine Reminder",
              message=f"Time for taking medication{med[1]}({med[2]})",
              timeout=10
            )

   
    threading.Timer(60, check_notification).start()

tk.Label(root, text="Medicine_Reminder", font=("Arial",15,"bold"), bg="#f0f0f0").pack(pady=10)

display_frame= tk.Frame(root, bg="#f0f0f0", padx=10,pady=10)

display_frame.pack(pady=20)

refresh_display()
tk.Button(root, text="Refresh", command=refresh_display, bg="#0000FF", fg="#FFFFFF").pack(pady=10)
tk.Button(root, text="Add Medication", command=open_add_window, bg="#00008B",fg="#FFFFFF").pack(pady=6)

threading.Thread(target=check_notification , daemon=True).start()

root.mainloop()