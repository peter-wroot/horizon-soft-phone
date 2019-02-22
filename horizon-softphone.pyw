import requests, time, os
from tkinter import Frame,Entry,Listbox,Tk,Button,Label,X,Y,GROOVE,SINGLE,END,S,N,SUNKEN,RAISED,RIDGE,BOTTOM
from selenium.webdriver import PhantomJS
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

def redial(index):
    app_window.phone_entry.delete(first=0,last=999)
    redial_number = app_window.history_list.get(first=index,last=index)
    app_window.phone_entry.insert(0,redial_number)

def initialize_webdriver():
    horizon_url = "https://www.unlimitedhorizon.co.uk/webapp/"
    initialize_webdriver.webdriver = PhantomJS()
    initialize_webdriver.webdriver.get(horizon_url)

def call(number):
    if(number != ""):
        app_window.phone_entry.delete(first=0,last=999)
        horizon_phone_entry = initialize_webdriver.webdriver.find_element_by_name("clickToDialNumber")
        horizon_phone_entry.clear()
        horizon_phone_entry.send_keys(number)
        horizon_call_button = initialize_webdriver.webdriver.find_element_by_name("ctdCall")
        horizon_call_button.send_keys(Keys.ENTER)
        app_window.history_list.insert(0,number.replace(" ",""))

def login(username,password):
    initialize_webdriver()
    horizon_username_entry = initialize_webdriver.webdriver.find_element_by_name("username")
    horizon_username_entry.send_keys(username)
    horizon_password_entry = initialize_webdriver.webdriver.find_element_by_name("password")
    horizon_password_entry.send_keys(password)
    horizon_login_button = initialize_webdriver.webdriver.find_element_by_name(":submit")
    horizon_login_button.send_keys(Keys.ENTER)
    app_window.login_button.config(state="disabled")
    app_window.username_entry.config(state="disabled")
    app_window.password_entry.config(state="disabled")
    app_window.phone_entry.config(state="normal")
    app_window.call_button.config(state="normal")
    app_window.history_list.config(state="normal")
    app_window.redial_button.config(state="normal")


def app_window():
    window = Tk()
    window.title("Horizon")
    window.configure(bg="white")
    window.resizable(width=False, height=False)
    window.grid_columnconfigure(1,weight=1)
    window.grid_rowconfigure(1,weight=1)
    if(os.path.exists('favicon.ico')):
        window.iconbitmap('favicon.ico')

    window_frame=Frame(window,bg="White")
    window_frame.pack(padx=5,pady=5)

    l_frame = Frame(window_frame,borderwidth=1,relief=SUNKEN)
    l_frame_bottom = Frame(window_frame,borderwidth=1,relief=SUNKEN)
    r_frame = Frame(window_frame,borderwidth=1,relief=SUNKEN)

    l_frame_inner=Frame(l_frame)
    l_frame_bottom_inner = Frame(l_frame_bottom)
    r_frame_inner=Frame(r_frame)

    r_frame_inner.pack(padx=5,pady=5,fill=Y)
    l_frame_inner.pack(padx=5,pady=5)
    l_frame_bottom_inner.pack(padx=5,pady=5)

    username_label = Label(l_frame_inner,text="Username")
    username_label.pack(fill=X)
    app_window.username_entry = Entry(l_frame_inner,width=30)
    app_window.username_entry.pack(pady=5)

    password_label = Label(l_frame_inner,text="Password")
    password_label.pack(fill=X)
    app_window.password_entry = Entry(l_frame_inner,show="*")
    app_window.password_entry.pack(pady=5,fill=X)

    app_window.login_button = Button(l_frame_inner,text="Login",relief=GROOVE,command=lambda: login(app_window.username_entry.get(),app_window.password_entry.get()))
    app_window.login_button.pack(fill=X)

    phone_label = Label(l_frame_bottom_inner,text="Phone Number")
    phone_label.pack()
    app_window.phone_entry = Entry(l_frame_bottom_inner,width=30)
    app_window.phone_entry.pack(pady=5)
    app_window.phone_entry.config(state="disabled")

    app_window.call_button = Button(l_frame_bottom_inner,text="Call",relief=GROOVE,command=lambda: call(app_window.phone_entry.get()))
    app_window.call_button.pack(fill=X)
    app_window.call_button.config(state="disabled")

    history_label = Label(r_frame_inner,text="Call History")
    history_label.pack()

    app_window.history_list= Listbox(r_frame_inner,relief=GROOVE,width=30,height=11)
    app_window.history_list.pack(pady=5)
    app_window.history_list.config(state="disabled")

    app_window.redial_button = Button(r_frame_inner,text="Redial",relief=GROOVE,command=lambda: redial(app_window.history_list.curselection()))
    app_window.redial_button.pack(fill=X)
    app_window.redial_button.config(state="disabled")

    l_frame.grid(column=0,row=0,padx=5,pady=5,stick=N)
    l_frame_bottom.grid(column=0,row=1,padx=5,pady=5,sticky=S)
    r_frame.grid(column=1,row=0,padx=5,pady=5,rowspan=2,sticky=N+S)

    window.mainloop()

app_window()