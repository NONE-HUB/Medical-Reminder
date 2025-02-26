import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk



root=Tk()
root.title("Image demo")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.minsize(400, 400)

image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")

def next_page(current_window):

    current_window.destroy()
            
    next = Toplevel(root)
    next.title("Welcome")
    next.geometry(f"{screen_width}x{screen_height}")
    next.minsize(400, 400) 

    image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
    bg_image=Label(next, image=image_path)
    bg_image.place(relheight=1,relwidth=1)

    frame = Frame(next, width =800 , height = 500 , bg = "white")
    frame.place(x=370, y=180)

    info_label = Label(frame, text="Enter your username and password", fg = "#57a1f8" , bg = "white" , font = ("Microsoft YaHei UI Light",32,"bold"))
    info_label.place(x = 25 )

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
        password_entry.delete(0, 'end')

    def on_leave(e):
        name=password_entry.get()
        if name == "":
            password_entry.insert(0,'Password')


    password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
    password_entry.place(x=200 , y = 305)
    password_entry.insert(0, "Password")
    password_entry.bind('<FocusIn>', on_enter)
    password_entry.bind('<FocusOut>', on_leave)
    Frame(frame, width=400,height=2,bg="black").place(x=200,y=348)

    def go_back():
        next.destroy()
        signin_screen()

    def go_home():
        next.destroy()
        root.deiconify()

    previous_button = Button(frame, text="Previous", width=25 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0,command=go_back)
    previous_button.place(x=30, y=420)

    next_button = Button(frame, text="Next" , width=25 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0,command=go_home)
    next_button.place(x=590 , y = 420)

    next.mainloop()

def signin_screen():

    root.withdraw()

    signin_screen = Toplevel(root)
    signin_screen.title("Welcome")
    signin_screen.geometry(f"{screen_width}x{screen_height}")
    signin_screen.minsize(400, 400) 

    image_path=PhotoImage(file=r"C:\Users\cis-c\OneDrive\Desktop\image\background_image.png")
    bg_image=Label(signin_screen, image=image_path)
    bg_image.place(relheight=1,relwidth=1)

    frame = Frame(signin_screen, width =800 , height = 500 , bg = "white")
    frame.place(x=370, y=180)

    info_label = Label(frame, text="Enter your information", fg = "#57a1f8" , bg = "white" , font = ("Microsoft YaHei UI Light",50,"bold"))
    info_label.place(x = 60 )


    def on_enter(e):
        firstname_entry.delete(0, 'end')

    def on_leave(e):
        name=firstname_entry.get()
        if name == "":
            firstname_entry.insert(0,'Firtsname')


    firstname_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
    firstname_entry.place(x=200 , y = 157)
    firstname_entry.insert(0, "Firstname")
    firstname_entry.bind('<FocusIn>', on_enter)
    firstname_entry.bind('<FocusOut>',on_leave)
    Frame(frame, width=400,height=2,bg="black").place(x=200,y=200)

    def on_enter(e):
        middlename_entry.delete(0, 'end')

    def on_leave(e):
        name=middlename_entry.get()
        if name == "":
            middlename_entry.insert(0,'Middlename')

        
    middlename_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
    middlename_entry.place(x=200 , y = 250)
    middlename_entry.insert(0, "Middlename")
    middlename_entry.bind('<FocusIn>', on_enter)
    middlename_entry.bind('<FocusOut>',on_leave)
    Frame(frame, width=400,height=2,bg="black").place(x=200,y=293)

    def on_enter(e):
        lastname_entry.delete(0, 'end')

    def on_leave(e):
        name=lastname_entry.get()
        if name == "":
            lastname_entry.insert(0,'Lastname')


    lastname_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
    lastname_entry.place(x=200 , y = 343)
    lastname_entry.insert(0, "Lastname")
    lastname_entry.bind('<FocusIn>', on_enter)
    lastname_entry.bind('<FocusOut>', on_leave)
    Frame(frame, width=400,height=2,bg="black").place(x=200,y=386)


    def go_back():
        signin_screen.destroy()
        root.deiconify()

    previous_button = Button(frame, text="Previous", width=25 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0,command=go_back)
    previous_button.place(x=30, y=420)

    next_button = Button(frame, text="Next" , width=25 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0,command=lambda: next_page(signin_screen))
    next_button.place(x=590 , y = 420)

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

        frame = Frame(reminder, width =800 , height = 500 , bg = "white")
        frame.place(x=370, y=180)

        add_label = Button(frame, text="Add",width=7 , fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center")
        add_label.place(x=20,y=30)

        edit_label = Button(frame, text="Edit",width=7 , fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center")
        edit_label.place(x=20,y=150)

        delete_label = Button(frame, text="Delete",width=7 , fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center")
        delete_label.place(x=20,y=270)

        update_label = Button(frame, text="Update",width=7 , fg="black" , border =0 , bg = "#57a1f8" , font = ("Microsoft YaHei UI Light",25) , justify="center")
        update_label.place(x=20,y=390)

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
    password = password_entry.get()

    if username == "username" and password == "password":
        home_page()

    else:
        messagebox.showerror("Invalid","Invalid username and password")

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
    password_entry.delete(0, 'end')

def on_leave(e):
    name=password_entry.get()
    if name == "":
        password_entry.insert(0,'Password')


password_entry = Entry(frame, width=25 , fg="black" , border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",22))
password_entry.place(x=200 , y = 305)
password_entry.insert(0, "Password")
password_entry.bind('<FocusIn>', on_enter)
password_entry.bind('<FocusOut>', on_leave)
Frame(frame, width=400,height=2,bg="black").place(x=200,y=348)

forgot_label = Label(frame, text="Forgot Password ?", fg="black",border =0 , bg = "white" , font = ("Microsoft YaHei UI Light",10) )
forgot_label.place(x=500, y = 353 )

signin_button = Button(frame, text="Sign in", width=80 , height=2 , pady=7, bg="#57a1f8", fg = "white" , border=0 , command= signin )
signin_button.place(x=110 , y = 400)

no_acc_label = tkinter.Label(frame, text="Don't have an account?" , fg = "black" , bg = "white" , font = ("Microsoft YaHei UI Light", 9))
no_acc_label.place(x = 305 , y = 456)

sign_up_label = Button(frame , text = "Sign up"  , width=6 ,  border =0 , bg = "white" , cursor = "hand2" , fg = "#57a1f8",command=signin_screen)
sign_up_label.place(x = 445 , y = 456)

root.mainloop()