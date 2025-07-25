from tkinter import *
import pandas as pd
import openpyxl
from openpyxl.drawing.image import Image as ExcelImage
from PIL import Image,ImageTk
from tkinter import filedialog
from tkinter import messagebox
import os

photo_path=""
file_path=os.path.join("./","vinayaka.xlsx")

def clear_all_fields():
    name.delete(0,END)
    rollno.delete(0,END)
    age.delete(0,END)
    email.delete(0,END)
    phone.delete(0,END)
    global photo_label
    photo_label.config(image='')


def retrieve_data(filtered_df):
    clear_all_fields()
    global label_under_search
    if filtered_df.empty:
        label_under_search.config(text="No student record found",bg="red",fg="white")
        return
    label_under_search.config(text="",bg="blue")
    name.insert(0,filtered_df["name"].values[0])
    rollno.insert(0,filtered_df["Rollno"].values[0])
    age.insert(0,filtered_df["age"].values[0])
    email.insert(0,filtered_df["email"].values[0])
    phone.insert(0,filtered_df["phone"].values[0])

    student_photo_path=filtered_df["photo_path"].values[0]

    

    if student_photo_path=="No Photo":
        photo_label.config(text="No Photo")
    else:
        student_image=Image.open(student_photo_path)
        student_image=student_image.resize((120,120))
        student_photo=ImageTk.PhotoImage(student_image)
        photo_label.config(image=student_photo)
        photo_label.name=student_photo

def search():
    rollno_search=search_box.get()
    dataframe=pd.read_excel(file_path,header=0)
    filtered_df=dataframe[dataframe["Rollno"]==rollno_search]
    retrieve_data(filtered_df)


def select_image():
    global new_photo_selected
    global photo_path
    photo_path=filedialog.askopenfilename(filetypes=[("Image Files","*.png;*.jpg;*.jpeg")])
    global new_photo_selected
    new_photo_selected=True
    if photo_path:
        img=Image.open(photo_path)
        img=img.resize((120,140))
        photo=ImageTk.PhotoImage(img)
        photo_label.config(image=photo)
        photo_label.image=photo


def create_workbook():
    workbook=openpyxl.Workbook()
    sheet=workbook.active
    sheet.append(["Rollno","name","age","email","phone","photo_path"])
    workbook.save(file_path)
    return sheet,workbook

def add():
    global photo_path
    rollno_data=rollno.get()
    name_data=name.get()
    age_data=age.get()
    email_data=email.get()
    phone_data=phone.get()
    if rollno_data=="" or name_data=="" or age_data==""or email_data==""or phone_data=="":
        msg_label.config(text="All fields are required",bg="red",fg="white")
        return
    
    if photo_path=="":
        photo_path="No Photo"
    if os.path.exists(file_path):
        workbook=openpyxl.load_workbook(file_path)
        sheet=workbook.active
    else:
        sheet,workbook=create_workbook()
    sheet.append([rollno_data,name_data,age_data,email_data,phone_data,photo_path])
    workbook.save(file_path)
    msg_label.config(text="Student added successfully",bg="green",fg="white")
    clear_all_fields()
    msg_label.after(2000,lambda:msg_label.config(text="",bg="blue"))


def update_top_level():
    global new_photo_selected
    new_photo_selected=False
    global update_rollno
    global update_top_level_window
    update_top_level_window=Toplevel(window)
    update_top_level_window.title("Update student")
    update_top_level_window.geometry("350x150+470+250")
    msg_label=Label(update_top_level_window,text="Enter the rollno of student to update",font=("bold"))
    msg_label.pack(pady=5) 
    update_top_level_window.focus_force()
    global label
    label=Label(update_top_level_window,text="")
    label.pack(pady=5)
    update_rollno=Entry(update_top_level_window,font=(12))
    update_rollno.pack(pady=5)
    update_rollno.focus()
    global enter_btn
    enter_btn=Button(update_top_level_window,text="Enter",command=update)
    enter_btn.pack()
    update_rollno.bind("<Return>",local_update_focus)

def local_update_focus(e):
    enter_btn.focus()
    update()

def update():
    update_no=update_rollno.get()
    if update_rollno.get()=="":
        label.config(text="Please enter a student rollno to update")
        return
    df=pd.read_excel(file_path,header=0)
    filtered_df=df[df["Rollno"]==update_no]
    if filtered_df.empty:
        label.config(text="No student matched for given rollno",fg="red")    
        return
    update_top_level_window.destroy()

    msg_label.config(text="",bg="blue")
    #setting all fields for the rollno
    retrieve_data(filtered_df)
    button_label.pack_forget()
    global update_button_frame
    update_button_frame=Frame(window,bg="blue",width=300,height=80)
    update_button_frame.place(x=100,y=470)
    update_button_frame.pack_propagate(False)
    global local_update_btn
    local_update_btn=Button(update_button_frame,text="update",font=(10),padx=3,command=lambda:update_data_excel(filtered_df))
    local_update_btn.place(x=50,y=25)
    global close_btn
    close_btn=Button(update_button_frame,text="close",font=(10),command=close,padx=7)
    close_btn.place(x=170,y=25)

def close():
    update_button_frame.destroy()
    button_label.pack(pady=10)
    

def update_data_excel(filtered_df):
    global update_button_frame
    update_button_label=Label(update_button_frame,text="Student data updated",bg="white",fg="green")
    update_button_label.place(x=70,y=5)
    idx=filtered_df.index[0]
    df=pd.read_excel(file_path,header=0)
    df.loc[idx,"Rollno"]=rollno.get()
    df.loc[idx,"name"]=name.get()
    df.loc[idx,"age"]=age.get()
    df.loc[idx,"email"]=email.get()
    df.loc[idx,"phone"]=phone.get()
    global new_photo_selected
    global photo_path
    if new_photo_selected==True:
        df.loc[idx,"photo_path"]=photo_path

    df.to_excel(file_path,index=False)

def delete_top_level():
    global delete_rollno
    global delete_top_level_window
    delete_top_level_window=Toplevel(window)
    delete_top_level_window.title("Update student")
    delete_top_level_window.geometry("350x150+470+250")
    msg_label=Label(delete_top_level_window,text="Enter the rollno of student to delete",font=("bold"))
    msg_label.pack(pady=5) 
    delete_top_level_window.focus_force()
    global delete_label
    delete_label=Label(delete_top_level_window,text="")
    delete_label.pack(pady=5)
    delete_rollno=Entry(delete_top_level_window,font=(12))
    delete_rollno.pack(pady=5)
    delete_rollno.focus()
    global delete_enter_btn
    delete_enter_btn=Button(delete_top_level_window,text="Enter",command=delete)
    delete_enter_btn.pack()
    delete_rollno.bind("<Return>",local_delete_focus)

def local_delete_focus(e):
    delete_enter_btn.focus()
    delete()

def delete():
    global delete_rollno
    del_rollno=delete_rollno.get()
    df=pd.read_excel(file_path)
    filtered_df=df[df["Rollno"]==del_rollno]
    if filtered_df.empty:
        delete_label.config(text="No students matched for that rollno",fg="red")
        return
    idx=filtered_df.index[0]
    df=df.drop(idx)
    df.to_excel(file_path,index=False)
    delete_label.config(text="Student deleted successfully",fg="purple")

window=Tk()
window.title("Student Information")
window.geometry("460x560+400+40")
student_icon_photo=Image.open(r"C:\Users\vinayaka\Coding\Python\student_information\student_title_bar_logo.jpg")
icon_photo=ImageTk.PhotoImage(student_icon_photo)
window.iconphoto(True,icon_photo)
window.config(bg="blue")

def search_func_call(e):
    search_button.focus()
    search()

search_box=Entry(window,width=20,font=(14))
search_box.pack(pady=5)
search_box.bind("<Return>",search_func_call)


search_button=Button(window,text="search",command=search)
search_button.place(x=355,y=7)

label_under_search=Label(window,text="",bg="blue")
label_under_search.pack()

photo_frame=Frame(window,width=140,height=170,bg="red")
photo_frame.pack(pady=5)
photo_frame.pack_propagate(False)
photo_add_btn=Button(photo_frame,text="Add photo",command=select_image)
photo_add_btn.pack()
photo_label=Label(photo_frame,bg="red")
photo_label.pack(fill="both",expand=True)

details_frame=Frame(window,bg="blue")
details_frame.pack(fill="both",expand="True",padx=5,pady=5)


name_label=Label(details_frame,text="Name",fg="white",bg="blue",font=('arial',12,"bold"),width=15)
name_label.grid(row=0,column=0,padx=5,pady=10)

name=Entry(details_frame,width=20,font=(5))
name.grid(row=0,column=1,pady=3)
name.focus()
name.bind("<Return>",lambda e:rollno.focus())
name.bind("<Down>",lambda e:rollno.focus())

rollno_label=Label(details_frame,text="Roll.no",fg="white",bg="blue",font=('arial',12,"bold"))
rollno_label.grid(row=1,column=0,padx=5,pady=10)
rollno=Entry(details_frame,width=20,font=(5))
rollno.grid(row=1,column=1,pady=3)
rollno.bind("<Up>",lambda e:name.focus())
for key in ("<Return>","<Down>"):
    rollno.bind(key,lambda e:age.focus())


age_label=Label(details_frame,text="Age",fg="white",bg="blue",font=('arial',12,"bold"))
age_label.grid(row=2,column=0,padx=5,pady=10)

age=Entry(details_frame,width=20,font=(5))
age.grid(row=2,column=1)
for key in ("<Return>","<Down>"):
    age.bind(key,lambda e:email.focus())
age.bind("<Up>",lambda e:rollno.focus())

email_label=Label(details_frame,text="Email",fg="white",bg="blue",font=('arial',12,"bold"))
email_label.grid(row=3,column=0,padx=5,pady=10)

email=Entry(details_frame,width=20,font=(5))
email.grid(row=3,column=1)
for key in("<Return>","<Down>"):
    email.bind(key,lambda e:phone.focus())
email.bind("<Up>",lambda e: age.focus())

phone_label=Label(details_frame,text="Phone.no",fg="white",bg="blue",font=('arial',12,"bold"))
phone_label.grid(row=4,column=0,padx=5,pady=10)

phone=Entry(details_frame,width=20,font=(5))
phone.grid(row=4,column=1)
phone.bind("<Return>",lambda e:add_button_focus(e))
phone.bind("<Up>",lambda e: email.focus())

def add_button_focus(e):
    add_btn.focus()
    add()


msg_label=Label(window,bg="blue",font=('arial',10,"bold"))
msg_label.pack()

button_label=Label(window,width=70,bg="blue")
button_label.pack(pady=10)
button_label.pack_propagate(False)

add_btn=Button(button_label,text="Add",font=(13),command=add,padx=20,activebackground="yellow")
add_btn.grid(row=0,column=0,padx=10)

update_btn=Button(button_label,text="Update",font=(13),command=update_top_level,activebackground="yellow")
update_btn.grid(row=0,column=1,padx=10)

delete_btn=Button(button_label,text="Delete",font=(13),command=delete_top_level,activebackground="yellow")
delete_btn.grid(row=0,column=2,padx=10)

window.mainloop()