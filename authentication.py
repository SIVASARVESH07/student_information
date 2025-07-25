import subprocess
from tkinter import *

def gui_authenticate():
    global authentication_window
    global username
    global password
    authentication_window=Tk()

    screen_width=authentication_window.winfo_screenwidth()
    screen_height=authentication_window.winfo_screenheight()

    x=(screen_width//2)-(300//2)
    y=(screen_height//2)-(240//2)

    authentication_window.geometry(f"300x170+{x}+{y}")
    authentication_window.title("Authentication")

    global msg
    msg=Label(authentication_window,text="Authentication",font=("bold"))
    msg.pack()

    frame=Frame(authentication_window,bg="blue")
    frame.pack(fill="both",expand=True)

    username_label=Label(frame,text="Username",font=("bold"),bg="blue",fg="white")
    username_label.grid(row=0,column=0,padx=10,pady=10)

    username=Entry(frame,width=13,font=("bold"))
    username.grid(row=0,column=1)
    username.focus()
    username.bind("<Return>",lambda e:password.focus())

    password_label=Label(frame,text="Password",font=("bold"),bg="blue",fg="white")
    password_label.grid(row=1,column=0)

    def auth_btn_focus(e):
        authenticate_btn.focus()
        authenticate()

    password=Entry(frame,width=13,font=("bold"),show="*")
    password.grid(row=1,column=1)
    password.bind("<Return>",auth_btn_focus)


    authenticate_btn=Button(authentication_window,text="authenticate",command=lambda:authenticate())
    authenticate_btn.pack(pady=10)

    authentication_window.mainloop()

def close_window_and_run_subprocess():
    authentication_window.destroy()
    subprocess.run(["python",r"C:\Users\vinayaka\Coding\Python\student_information\main.py"],creationflags=subprocess.CREATE_NO_WINDOW)
    
def authenticate():
    global username,password
    if username.get()=="vinayaka" and password.get()=="siva":
        print("Hello World")
        msg.config(text="Authentication successfull",fg="green")
        authentication_window.after(5000,close_window_and_run_subprocess)
    else:
        msg.config(text="Authentication failed",fg="red")
        return
gui_authenticate()
