# Import required libraries
import requests, time, os
from tkinter import Frame,Entry,Listbox,Tk,Button,Label,X,Y,GROOVE,SINGLE,END
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

# When the user wants to redial a number, we look it up based
# on its index in the Listbox, then empty out the input field
# and enter the chosen phone number.
def redial_number(num):
    setup_window.phone_number_input.delete(first=0,last=999)
    redial_num = setup_window.past_call_list.get(first=num,last=num)
    setup_window.phone_number_input.insert("end",redial_num)

# Creates the WebDriver object and opens the Horizon login URL
def init_webdriver():
    horizon_url = "https://www.unlimitedhorizon.co.uk/webapp/"
    web_driver_options = Options()
    web_driver_options.add_argument("-headless")
    init_webdriver.web_driver = Firefox(executable_path="geckodriver", options=web_driver_options)
    init_webdriver.web_driver.get(horizon_url)

def setup_window():
    # Creates the window and sets the title and icon (if it exists), sets the 
    # resizability to False, and sets the function to run when
    # The window is closed. 
    setup_window.window_root = Tk()
    setup_window.window_root.wm_title("Horizon")

    if(os.path.exists('favicon.ico')):
        setup_window.window_root.iconbitmap('favicon.ico')

    setup_window.window_root.resizable(width=False, height=False)
    setup_window.window_root.protocol("WM_DELETE_WINDOW",on_close)

    # Creates the various frames that are used to hold the content.
    # One from the left-hand column, and one for the right. 
    left_col_frame = Frame(setup_window.window_root)
    right_col_frame = Frame(setup_window.window_root)

    # Creates the various widgets for the application
    user_name_label = Label( left_col_frame,text="Horizon Username")
    setup_window.user_name_field = Entry( left_col_frame,relief=GROOVE)
    password_label = Label( left_col_frame,text="Horizon Password")
    setup_window.password_field = Entry( left_col_frame,show="*",relief=GROOVE)
    setup_window.login_button = Button( left_col_frame,text="Login",relief=GROOVE,command=lambda: horizon_login(setup_window.user_name_field.get(),setup_window.password_field.get()))
    phone_number_label = Label( left_col_frame, text="Phone Number")
    setup_window.phone_number_input = Entry( left_col_frame,relief=GROOVE,state="disabled")
    setup_window.call_button = Button( left_col_frame,text="call",relief=GROOVE,state="disabled",command=lambda: call_number(setup_window.phone_number_input.get()))
    past_call_label = Label(right_col_frame,text="Call History")
    setup_window.past_call_list = Listbox(right_col_frame,selectmode=SINGLE,yscrollcommand=True,relief=GROOVE,height=9)
    redial_button = Button(right_col_frame,text="Redial",relief=GROOVE,command=lambda: redial_number(setup_window.past_call_list.curselection()))

    # Packs the widgets for the left-hand grid column, and then
    # puts the frame into the grid as column 0
    left_col_top_blank = Label( left_col_frame)
    left_col_top_blank.pack()
    user_name_label.pack(fill=X)
    setup_window.user_name_field.pack(fill=X,padx=10)
    password_label.pack(fill=X)
    setup_window.password_field.pack(fill=X,padx=10)
    setup_window.login_button.pack(fill=X,padx=10)
    left_col_mid_blank = Label( left_col_frame)
    left_col_mid_blank.pack()
    phone_number_label.pack(fill=X)
    setup_window.phone_number_input.pack(fill=X,padx=10)
    setup_window.call_button.pack(fill=X,padx=10)
    left_col_end_blank = Label( left_col_frame)
    left_col_end_blank.pack()
    left_col_frame.grid(column=0,row=0)

    # Packs the widgets into the right-hand column, and then
    # puts the frame into the grid as column 1
    right_col_top_blank = Label(right_col_frame)
    right_col_top_blank.pack()
    past_call_label.pack(fill=X)
    setup_window.past_call_list.pack(fill=X,padx=10)
    redial_button.pack(fill=X,padx=10)
    right_col_end_blank = Label(right_col_frame)
    right_col_end_blank.pack()
    right_col_frame.grid(column=1,row=0)

    setup_window.window_root.mainloop()

# When the window is closed, we 'destroy' it, and close the 
# webdriver so we don't leave background processes running. 
def on_close():
    setup_window.window_root.destroy()
    init_webdriver.web_driver.close()

# Sends the entered phone number to the webdriver and then
# Clicks the 'call' button, before blanking out the number field. 
def call_number(n):
    setup_window.phone_number_input.delete(first=0,last=999)
    phone_number_field = init_webdriver.web_driver.find_element_by_name("clickToDialNumber")
    phone_number_field.send_keys(n)
    dial_button = init_webdriver.web_driver.find_element_by_name("ctdCall")
    dial_button.send_keys(Keys.ENTER)
    setup_window.past_call_list.insert(END,n)

# Runs the init_webdriver function, and then passes the username
# and password to the Webdriver, and clicks the 'login' button. The
# username, password, and login button widgets are then disabled. 
def horizon_login(u,p):

    init_webdriver()
    
    username_field_web = init_webdriver.web_driver.find_element_by_name("username")
    username_field_web.send_keys(u)
    password_field_web = init_webdriver.web_driver.find_element_by_name("password")
    password_field_web.send_keys(p)
    login_button_web = init_webdriver.web_driver.find_element_by_name(":submit")
    login_button_web.send_keys(Keys.ENTER)
    setup_window.user_name_field.config(state="disabled")
    setup_window.password_field.config(state="disabled")
    setup_window.login_button.config(state="disabled")
    time.sleep(10)
    setup_window.call_button.config(state="normal")
    setup_window.phone_number_input.config(state="normal")

# Runs the setup_window function.
setup_window()

