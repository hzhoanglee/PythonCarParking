import customtkinter as ttk
import tkinter as tk
from tkinter import ttk as ttkz
from tkinter import *
from PIL import Image
from time import strftime
from ManSys import ManagementSystem
from tkinter import messagebox as mbox
from utils.connect import mydb

ms = ManagementSystem()
ms.setup_parking_lot()


class ParkingFloor:
    def __init__(self, floor_code, floor_slots):
        self.floor_code = floor_code
        self.floor_slots = floor_slots

    def set_floor_code(self, floor_code):
        self.floor_code = floor_code

    def get_floor_code(self):
        return self.floor_code

    def set_floor_slots(self, floor_slots):
        self.floor_slots = floor_slots

    def get_floor_slots(self):
        return self.floor_slots


# Setting the theme for the main window
ttk.set_appearance_mode('light')
mainColor = "#8685ef"
sideColor = "#faf8ff"
mainScreenColor = '#f2ecff'
frameColor = '#e9e1ff'
grayColor = '#737373'
hoverColor = '#ccccff'

# Setting the main window
root = ttk.CTk()
root.geometry('970x700')
root.resizable(True, True)
root.title("Vịt Quay Parking System")
root.config(background='#f2ecff')


# ================================================
# ===================FUNCTIONS====================
# ================================================

# Creating date/time
def my_time():
    time_string = strftime('%H:%M:%S %p \n %A \n %x')
    l1.configure(text=time_string)
    l1.after(1000, my_time)  # time delay of 1000 milliseconds


# New window when a sidebar button is clicked
def open_check_in(slot_code="Auto"):
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Car Check In Window")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 300, y + 150))
    new.geometry('500x450')

    # form
    label = ttk.CTkLabel(master=new,
                         text="Car Check In",
                         text_color=grayColor,
                         font=('', 20, 'bold'),
                         fg_color=mainScreenColor, ).place(x=100, y=90)

    driverName = ttk.CTkEntry(master=new,
                              width=300,
                              height=40,
                              placeholder_text='Driver Name',
                              bg_color=mainScreenColor)
    driverName.place(x=100, y=140)

    licensePlate = ttk.CTkEntry(master=new,
                                width=300,
                                height=40,
                                placeholder_text='License plate',
                                bg_color=frameColor
                                )
    licensePlate.place(x=100, y=195)

    # Getting slot codes
    slot_codes = ['Auto']
    lst = ms.get_unused_slots()
    for slot in lst:
        slot_codes.append(str(slot.get_slot_code()))

    # Dropdown box
    dropdown = ttk.CTkOptionMenu(master=new,
                                 height=40,
                                 values=slot_codes,
                                 button_color=mainColor,
                                 fg_color=mainColor,
                                 button_hover_color=hoverColor,
                                 dropdown_hover_color=hoverColor
                                 )
    dropdown.set(slot_code)
    dropdown.place(x=100, y=250)

    def submit():
        # Check if all fields are filled out
        if driverName.get() and licensePlate.get() and dropdown.get():
            # Check if dropdown menu has a value selected
            if dropdown.get() != "Auto":
                # Add car
                ms.checkin(driverName.get(), licensePlate.get(), dropdown.get())
                # Show success message
                mbox.showinfo("Success", "A car has been added.")
                # Close the Toplevel window
                new.destroy()
            else:
                # Show error message
                mbox.showerror("Error", "Please select a parking slot.")
        else:
            # Show error message
            mbox.showerror("Error", "Please input everything.")

    # Submit button
    submitButton = ttk.CTkButton(master=new,
                                 height=40,
                                 text="Add car",
                                 fg_color=mainColor,
                                 font=("", 15, 'bold'),
                                 text_color='white',
                                 cursor="hand2",
                                 hover_color='#ccccff', command=lambda: submit())
    submitButton.place(x=100, y=320)

    # Keep the toplevel window in front of the root window
    new.wm_transient(root)
    new.mainloop()


def open_check_out(slot_code):
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Car Check Out Window")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 300, y + 150))
    new.geometry('500x450')

    # form
    label = ttk.CTkLabel(master=new,
                         text="Car Check Out",
                         text_color=grayColor,
                         font=('', 20, 'bold'),
                         fg_color=mainScreenColor, ).place(x=100, y=90)

    # Getting slot codes
    slot_codes = [slot_code]
    lst = ms.get_used_slots()
    for slot in lst:
        print(slot)
        #slot_codes.append(str(slot.get_slot_code()))

    # Dropdown box
    dropdown = ttk.CTkOptionMenu(master=new,
                                 height=40,
                                 values=slot_codes,
                                 button_color=mainColor,
                                 fg_color=mainColor,
                                 button_hover_color=hoverColor,
                                 dropdown_hover_color=hoverColor
                                 )
    dropdown.set(slot_code)
    dropdown.place(x=100, y=250)

    def checkout_submit():
        if dropdown.get():
            if dropdown.get() != "Auto":
                price = ms.checkout(dropdown.get())
                check_out_text = "Check Out success. Total price: " + str(price)
                mbox.showinfo("Success", check_out_text)
                new.destroy()
            else:
                mbox.showerror("Error", "Please select a parking slot.")
        else:
            # Show error message
            mbox.showerror("Error", "Please input everything.")

    # Submit button
    submitButton = ttk.CTkButton(master=new,
                                 height=40,
                                 text="Check Out",
                                 fg_color=mainColor,
                                 font=("", 15, 'bold'),
                                 text_color='white',
                                 cursor="hand2",
                                 hover_color='#ccccff', command=lambda: checkout_submit())
    submitButton.place(x=100, y=320)

    # Keep the toplevel window in front of the root window
    new.wm_transient(root)
    new.mainloop()


def open_manage():
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Manage Car Window")
    new.config(background=mainScreenColor)
    #x = root.winfo_x()
    #y = root.winfo_y()
    #new.geometry("+%d+%d" % (x + 250, y + 100))
    new.geometry('600x520')

    # Connect to DB
    new.dbconnection = mydb.cursor()
    new.dbconnection.execute("SELECT * FROM check_ins")

    # CSS
    style = ttkz.Style()
    style.configure("Treeview",
                    background = "#f9f9f9",
                    foreground="#6f727a",
                    fieldbackground = "#ddeaef",
                    rowheight= 60,
                    borderwidth = 5,
                    border = "#6f727a",
                    font=(None, 12))

    style.configure("Treeview.Heading",
                    background="#d7d2ea",
                    rowheight= 80,
                    foreground = "#6f727a",
                    font= ("Bold", 14))

    # Row settings
    tree = ttkz.Treeview(new, height=10)

    # Delete blank column
    tree["show"] = 'headings'

    # Define columns number
    tree["columns"] = ("id", "plate", "owner", "checkin", "checkout", "status", "slot")

    # Individual column size
    tree.column("id", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("plate", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("owner", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("checkin", width=200, minwidth=200, anchor=tk.CENTER)
    tree.column("checkout", width=200, minwidth=200, anchor=tk.CENTER)
    tree.column("status", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("slot", width=150, minwidth=150, anchor=tk.CENTER)

    # Columns name
    tree.heading("id", text="ID", anchor=tk.CENTER)
    tree.heading("plate", text="License Plate", anchor=tk.CENTER)
    tree.heading("owner", text="Driver Name", anchor=tk.CENTER)
    tree.heading("checkin", text="Check-in Time", anchor=tk.CENTER)
    tree.heading("checkout", text="Check-out Time", anchor=tk.CENTER)
    tree.heading("status", text="Occupied", anchor=tk.CENTER)
    tree.heading("slot", text="Slot Code", anchor=tk.CENTER)

    #
    i = 0
    for ro in new.dbconnection:
        tree.insert("", i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
        i += 1

    # Scroll bar
    hsb = ttkz.Scrollbar(new, orient="horizontal")
    hsb.configure(command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.pack(fill=X, side=BOTTOM)

    vsb = ttkz.Scrollbar(new, orient="vertical")
    vsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(fill=Y, side=RIGHT)

    tree.pack()

    # Real-time counter
    # Used slot
    used_slot = ms.get_used_slot_count()
    lab1 = Label(new, font=("#6f727a", 14, "bold"), width=15,
                 height=2,
                 text = "Occupied slots : ")
    lab1.place(x=60, y=670)
    lab2 = Label(new, font=("#6f727a", 16, "bold"),
                 width=15,
                 height=2,
                 text=used_slot)
    lab2.place(x=250, y=670)

    # Available slots
    avail_slot = ms.get_available_slot_count()
    lab3 = Label(new, font=("#6f727a", 14, "bold"), width=15,
                 height=2,
                 text="Available slots : ")
    lab3.place(x=460, y=670)
    lab4 = Label(new, font=("#6f727a", 16, "bold"),
                 width=15,
                 height=2,
                 text=avail_slot)
    lab4.place(x=650, y=670)


    new.wm_transient(root)
    new.mainloop()


class ParkingBuildingGUI:
    def __init__(self):
        self.building_settings = ms.get_settings()
        floor_count = int(self.building_settings.get_Z_VALUE())
        self.building_floors = []
        for i in range(floor_count):
            floor_code = f"F{i}"
            floor_slots = []
            for slot in ms.get_slot_list():
                if slot.get_slot_code().endswith(floor_code):
                    floor_slots.append(slot)
            self.building_floors.append(ParkingFloor(floor_code, floor_slots))

        self.x_list = []
        for i in range(int(self.building_settings.get_X_VALUE())):
            chars = [chr(i + 65)]
            self.x_list.append(chars)

        self.y_list = []
        for i in range(int(self.building_settings.get_Y_VALUE())):
            self.y_list.append(i)

    def main_section(self):
        # Print main window in the right of sidebar
        main = ttk.CTkFrame(master=root, width=500,
                            height=1300)
        main.place(x=233, y=100)

        # Customize the floor buttons
        s = ttkz.Style()
        s.theme_use('default')
        s.configure('TNotebook.Tab',font =("clam", 12, "bold"), width=15, height=100, background="#E0E0E0")
        s.map("TNotebook", background=[("selected", "pink")])

        tab_control = ttkz.Notebook(main)
        for floor in self.building_floors:
            tab = ttkz.Frame(tab_control)
            tab_control.add(tab, text=floor.get_floor_code())
            tab_control.pack(padx=5, pady=10, expand=10, fill="both")
            self.floor_window(tab, floor)

    def floor_window(self, tab, floor):
        slot_button_list = []
        for slot in floor.get_floor_slots():
            # Text with slot code and check if available
            if slot.is_available():
                text = slot.get_slot_code() + "\nOpen"
                color = '#408E91'
            else:
                text = slot.get_slot_code() + "\nOccupied"
                color = '#E49393'

            slot_button = ttk.CTkButton(tab, text=text, fg_color=color, width=120, height=80,
                                        font=("", 15, 'bold'),
                                        text_color='white',
                                        cursor="hand2",
                                        hover_color='#ccccff',
                                        command=lambda slot_code=slot.get_slot_code(): self.slot_window(slot_code))

            slot_button_list.append(slot_button)

        # use grid to place buttons in a table
        for i in range(len(slot_button_list)):
            row = i // len(self.x_list)
            col = i % len(self.x_list)
            slot_button_list[i].grid(row=row, column=col)
            slot_button_list[i].grid(padx=10, pady=10)

    def slot_window(self, slot_code):
        slot = ms.get_slot_by_code(slot_code)
        if slot.is_available():
            open_check_in(slot_code)
        else:
            open_check_out(slot_code)
        self.re_init()
        self.main_section()

    def re_init(self):
        self.building_settings = ms.get_settings()
        floor_count = int(self.building_settings.get_Z_VALUE())
        self.building_floors = []
        for i in range(floor_count):
            floor_code = f"F{i}"
            floor_slots = []
            for slot in ms.get_slot_list():
                if slot.get_slot_code().endswith(floor_code):
                    floor_slots.append(slot)
            self.building_floors.append(ParkingFloor(floor_code, floor_slots))

        self.x_list = []
        for i in range(int(self.building_settings.get_X_VALUE())):
            chars = [chr(i + 65)]
            self.x_list.append(chars)

        self.y_list = []
        for i in range(int(self.building_settings.get_Y_VALUE())):
            self.y_list.append(i)



# ================================================
# ===================END OF FUNCTIONS=============
# ================================================

# ====================================
# =============HEADER=================
# ====================================

# Creating the header
header = ttk.CTkFrame(root,
                      width=1070,
                      height=60,
                      fg_color="#8685ef")
header.place(x=201, y=0)

# Log out button
logout_text = ttk.CTkButton(header,
                            text="Logout",
                            font=("", 13, "bold"),
                            fg_color='white',
                            cursor='hand2',
                            text_color=mainColor,
                            hover_color='#ccccff')
logout_text.place(x=588, y=15)

# ====================================
# =============END OF HEADER==========
# ====================================

# ===============================================
# =====================SIDEBAR===================
# ===============================================

# Sidebar
sideBar = ttk.CTkFrame(master=root, width=200,
                       height=1300,
                       fg_color="#faf8ff")
sideBar.place(x=0, y=0)

# Logo
logoImage = ttk.CTkImage(light_image=Image.open("images/icon.png"),
                         size=(100, 100))
logo = ttk.CTkLabel(sideBar,
                    text='',
                    image=logoImage)
logo.place(x=50, y=80)

# Name of the person
name = ttk.CTkLabel(master=sideBar,
                    text="ADMIN",
                    font=("", 15, "bold"),
                    text_color="#737373")
name.place(x=75, y=180)

# ===============================================
# =====================BUTTONS===================
# ===============================================

# Car check in
carImage = ttk.CTkImage(light_image=Image.open('images/car.png'),
                        size=(25, 25))

carButton = ttk.CTkButton(master=sideBar,
                          image=carImage,
                          text="Car check-in",
                          width=200,
                          height=50,
                          compound='left',
                          fg_color='transparent',
                          text_color=mainColor,
                          font=('', 15, 'bold'),
                          cursor="hand2",
                          anchor='center',
                          hover_color='#ccccff',
                          command=lambda: open_check_in(),
                          ).place(x=0, y=250)

# Manage vehicle

manageImage = ttk.CTkImage(light_image=Image.open('images/manage.png'),
                           size=(20, 20))
manageButton = ttk.CTkButton(master=sideBar,
                             image=manageImage,
                             text="Manage vehicle",
                             width=200,
                             height=50,
                             compound='left',
                             fg_color='transparent',
                             text_color=mainColor,
                             font=('', 15, 'bold'),
                             cursor="hand2",
                             anchor='center',
                             hover_color='#ccccff',
                             command=lambda: open_manage()
                             ).place(x=0, y=300)

# ===============================================
# =====================END OF BUTTONS============
# ===============================================

# ===============================================
# =====================TIME======================
# ===============================================


l1 = ttk.CTkLabel(master=sideBar, font=('', 15, 'bold'), text_color=grayColor)
l1.place(x=50, y=400)

# ===============================================
# =====================END OF TIME===============
# ===============================================

# ======================================================
# =====================END OF SIDEBAR===================
# ======================================================


# ======================================================
# =====================MAIN SCREEN======================
# ======================================================

# display to main screen something
gui = ParkingBuildingGUI()
gui.main_section()
my_time()
root.mainloop()