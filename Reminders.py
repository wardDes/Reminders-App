from tkinter import *
import tkcalendar
from tkcalendar import Calendar, DateEntry
import win10toast
from win10toast import ToastNotifier
import datetime
from datetime import datetime, date, timedelta
import time as tm
from time import localtime, strptime, strftime
from tkinter.font import Font
from tkinter import filedialog
import pickle
import sys,re,os
import babel.numbers

root = Tk()
root.title('Reminders')

from os import path

bundle_dir = path.abspath(path.dirname(__file__))
path_to_dat = path.join(bundle_dir, "myschedule.dat")

path_to_ico = path.join(bundle_dir, "dh.ico")

root.geometry("811x626")

root.iconbitmap(path_to_ico)
root_frame=Frame(root)
root_frame.pack()

global reminders
reminders = []

app_font = Font(
    family = "Sans Serif",
    size=16,
    weight="bold",
    underline=False
)


time_frame =Frame(root_frame, bg="#e4e4e4")
time_frame.grid(row=2,column=0,columnspan=4, ipady=1)

cal = Calendar(root_frame, 
        selectmode= "day",
        date_pattern="mm/dd/y",
        day=date.today().day,
        firstweekday="sunday")

        

cal.grid(row=0, column=0, 
                columnspan=4, 
                padx=(15, 45))


def get_date():
    my_label.config(text=cal.get_date())
    global my_date
    my_date = cal.get_date()
    cal_date = cal.get_date()# IMPORTANT
    

st_tm_lbl = Label(root, text="")
st_tm_lbl.config(font=app_font)
st_tm_lbl.pack()

item =StringVar()
item = ""

def add_item():
    hr = hrs_spin.get()
    min =mins_spin.get()
    tm_day = am_pm_spin.get()
    time =hr+':'+min
    date = cal.get_date()

    app_error_font = Font(
        family = "Sans Serif",
        size=16,
        weight="bold"
    )

    st_tm_lbl["text"]= date + " " + time + " " + tm_day + " " + msg_entry.get()

    item_date = strptime(date + " " + time + ":00" + tm_day, "%m/%d/%Y %I:%M:%S%p")
    
    my_year = item_date.tm_year
    my_month = item_date.tm_mon
    my_day =item_date.tm_mday
    my_hour = item_date.tm_hour
    my_min = item_date.tm_min
    my_datetime = datetime(my_year,my_month,my_day,my_hour,my_min)
    
    #check for not word characters from entry
    ltr_chars_onlyrgx = re.compile(r'[\^\$\*\+\?\{\}\[\]\\\|\(\)]')
    msg = msg_entry.get()
    res = ltr_chars_onlyrgx.findall(msg)



    # check if entry is empty
    if msg_entry.get() == "":
        st_tm_lbl["text"] = "Please enter reminder text"
        st_tm_lbl.config(fg="red")
        return
    elif len(res) >= 1:
        st_tm_lbl["text"] = "Please only enter word characters and spaces"
        st_tm_lbl.config(fg="red")
        res=[]
        msg_entry.delete(0,END)
        return
    else:
        st_tm_lbl.config(fg="black")

    reminder = [date, time, tm_day, msg_entry.get(), my_datetime]
    
    reminders.append(reminder)
    
    msg_entry.delete(0,END)
   

    # clear listbox
    rem_listbx.delete(0, END)

    reminders_sorted =sorted(reminders, key=lambda x: (x[4]))
    
    for item in reminders_sorted:
        item_str = f'{item[0]}, {item[1]}, {item[2]}, {item[3]}'
        rem_listbx.insert(END, item_str)
    save_reminders()

spin_val_hrs = ["01","02","03","04","05","06","07","08","09","10","11","12"]
spin_val_mins = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
spin_am_pm = ["AM","PM"]

msg_text = StringVar()
msg_entry = Entry(time_frame, textvariable=msg_text, width=40, bd=0)
msg_entry.grid(row=2, column=5, sticky="w", padx=5)

hrs_lbl = Label(time_frame, text="Hours", bd=0)
hrs_lbl.config(font=app_font)
hrs_lbl.grid(row=2,column=0, sticky="w")

mins_lbl = Label(time_frame, text="Minutes",bd=0)
mins_lbl.config(font=app_font)
mins_lbl.grid(row=2, column=2, sticky="w")

hrs_spin_var = StringVar()

mins_spin_var = StringVar()

spin_am_pm_var = StringVar()

hrs_spin = Spinbox(time_frame, values=spin_val_hrs, state='readonly', wrap=True, textvariable=hrs_spin_var, width=2, bd=0)
hrs_spin.config(font=app_font)
mins_spin = Spinbox(time_frame, values=spin_val_mins, state='readonly', wrap=True, textvariable=mins_spin_var, width=2, bd=0)
mins_spin.config(font=app_font)
am_pm_spin = Spinbox(time_frame, values=spin_am_pm, state='readonly', wrap=True, textvariable=spin_am_pm_var, width=4, bd=0)
am_pm_spin.config(font=app_font)

tmnow = tm.strftime("%I:%M: %p")
tmnowlst = tmnow.split(':')
hour = tmnowlst[0]
minet = tmnowlst[1]
tod = tmnowlst[2].strip()


index = spin_val_hrs.index(hour)
hrs_spin_var.set(spin_val_hrs[index])

index = spin_val_mins.index(minet)
mins_spin_var.set(spin_val_mins[index])

index = spin_am_pm.index(tod)
spin_am_pm_var.set(spin_am_pm[index])


hrs_spin.grid(row=2, column=1, sticky="w", padx=5)
mins_spin.grid(row=2,column=3, sticky="w",padx=5)
am_pm_spin.grid(row=2,column=4, sticky="w",padx=5)



dsply_lbl = Label(root_frame, text="Select Date, Time and enter Reminder Message")
dsply_lbl.grid(row=1,column=0,columnspan=4)




def deleteItem():
    # insure user selects an item before
    # clicking delete button
    try:
        cur_index = rem_listbx.curselection()[0]
    except Exception as ex:
        st_tm_lbl["text"] = "Select a reminder to delete"
        st_tm_lbl.config(fg="red")
        return
    # remove selected delete item from reminders
    val = rem_listbx.get(rem_listbx.curselection())# returns tuple
    idx = rem_listbx.get(0, END).index(val)
    global reminders
    cur_reminder_item = reminders[idx]
    del reminders[idx]

    # clear listbox
    rem_listbx.delete(0, END)

    reminders_sorted =sorted(reminders, key=lambda x: (x[4]))
    reminders = reminders_sorted

    for item in reminders:
        item_str = f'{item[0]}, {item[1]}, {item[2]}, {item[3]}'
        rem_listbx.insert(END, item_str)
    
    save_reminders()

def editItem():# Edit
    # insure user selects an item before
    # clicking edit button
    try:
        cur_index = rem_listbx.curselection()[0]
    except Exception as ex:
        st_tm_lbl["text"] = "Select a reminder to edit"
        st_tm_lbl.config(fg="red")
        return
    
    val = rem_listbx.get(rem_listbx.curselection())# returns tuple
    
    # GET INDEX OF SELECTED ITEm
    idx = rem_listbx.get(0, END).index(val)
    global reminders
    cur_reminder_item = reminders[idx]
    
    # DELETE FROM REMINDERS LIST
    del reminders[idx]
    
    # clear listbox
    rem_listbx.delete(0, END)
  
    # sort items
    reminders_sorted =sorted(reminders, key=lambda x: (x[4]))
    reminders = reminders_sorted

    for item in reminders:
        item_str = f'{item[0]}, {item[1]}, {item[2]}, {item[3]}'
        rem_listbx.insert(END, item_str)

    msg_entry.delete(0, END)

    #make val into a list and get message from list
    val_lst = val.split(',')
    msg_str = val_lst[3]

    msg_entry.insert(0, msg_str)
    save_reminders()


lstbx_frame = Frame(root_frame, width=500)
lstbx_frame.grid(row=3,column=0,columnspan=4, ipady=1, pady=10)

my_scrollbar = Scrollbar(lstbx_frame) 
my_scrollbar.pack(side=RIGHT, fill=BOTH)

my2_scrollbar = Scrollbar(lstbx_frame)
my2_scrollbar.pack(side=BOTTOM, fill=X)

rem_listbx = Listbox(lstbx_frame, listvariable=item,
              font = app_font,
              width=60,
              height=10,
              activestyle=NONE,
              highlightthickness=0, 
              bd=0,
              selectbackground="#4e4e4e")

rem_listbx.pack(side=LEFT, fill=BOTH)

rem_listbx.config(yscrollcommand = my_scrollbar.set)
my_scrollbar.config(command=rem_listbx.yview)

rem_listbx.config(xscrollcommand = my2_scrollbar.set)
my2_scrollbar.config(command=rem_listbx.xview)


btn_frame = Frame(root_frame)
btn_frame.grid(row=4,column=0,columnspan=4, ipady=1, pady=10)


set_tm_btn = Button(btn_frame, text="Set Reminder", command=add_item)
set_tm_btn.config(font=app_font)
set_tm_btn.grid(row=0, column=2, padx=5)

mybtn3 = Button(btn_frame, text="Edit Item", command=editItem)
mybtn3.config(font=app_font)
mybtn3.grid(row=0, column=3, padx=5)


mybtn6 = Button(btn_frame, text="Delete Item", command=deleteItem)
mybtn6.config(font=app_font)
mybtn6.grid(row=0, column=4, padx=5)

def save_reminders():
    file_name = path_to_dat
    output_file = open(file_name, 'wb')
    global reminders
    reminders_sorted =sorted(reminders, key=lambda x: (x[4]))
    reminders = reminders_sorted
    pickle.dump(reminders, output_file)
    

def open_reminders():
    global reminders

    file_name = path_to_dat
    print(file_name)

    input_file = open(file_name, 'rb')
    try:
        reminders = pickle.load(input_file)
    except:
        pass
    
    reminders_sorted =sorted(reminders, key=lambda x: (x[4]))
    
    reminders = reminders_sorted
    for item in reminders:
        item_str = f'{item[0]}, {item[1]}, {item[2]}, {item[3]}'
        rem_listbx.insert(END, item_str)

    input_file.close()
    

# after cancel
c_id = ""

def get_now_time(default=None):
    # create datetime struct of current time
    cur_time = strftime("%Y-%m-%d %I:%M:%S%p", localtime())

    cur_time_date = strptime(cur_time, "%Y-%m-%d %I:%M:%S%p")


    my_year = cur_time_date.tm_year
    my_month = cur_time_date.tm_mon
    my_day =cur_time_date.tm_mday
    my_hour = cur_time_date.tm_hour
    my_min = cur_time_date.tm_min

    # create datetime from time.struct values
    my_datetime = datetime(my_year,my_month,my_day,my_hour,my_min)
    
    return my_datetime


def app_notify():
    toaster = ToastNotifier()
    try:
        toaster.show_toast(
            "Reminder",
            my_message,
            icon_path=path_to_ico,
            duration=50,
            threaded=True)
    except Exception as ex:
        print("Error: ", type(ex),ex.args)
    
    

def start_app():
    note_timer()




def chkMsgDts():
    comparedate = get_now_time()
    
    for i in reminders:
        # get datetime for each reminder
        item_date = i[4]
        
        # evoke notification
        global title
        global my_message
        global my_app_name
        title = 'Reminder'
        my_message=i[3]
        my_app_name = "Reminders"

        # add 1 minute to current time
        comparedate_plus1 = comparedate + timedelta(seconds=60)
       
        # call notify when reminder date/time
        # is equal to approx 60 seconds curr date/time
        global toggle
        if (comparedate_plus1 == item_date):
            app_notify()
           

def note_timer():
    # funtion to check date/times of reminder els
    chkMsgDts()
    
    # get stop object for timer
    global c_id
    c_id = root.after(59000, note_timer)
    


# stop timer
def close(event):
    timer_stop(c_id)
    #sys.exit()

root.bind('<Escape>', close)

open_reminders()

# start timer
start_app()

root.mainloop()
