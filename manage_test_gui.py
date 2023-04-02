import customtkinter as ttk
import tkinter as tk
from tkinter import ttk as ttkz
from PIL import Image
from time import strftime
from ManSys import ManagementSystem
from tkinter import messagebox as mbox

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
root.geometry('1020x700')
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


def open_manage():
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Manage Car Window")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 250, y + 100))
    new.geometry('600x520')

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
        main.place(x=220, y=100)
        tab_control = ttkz.Notebook(main)
        for floor in self.building_floors:
            tab = ttkz.Frame(tab_control)
            tab_control.add(tab, text=floor.get_floor_code())
            tab_control.pack(expand=1, fill="both")
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
            print("WTF")


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
logout_text.place(x=450, y=15)

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

# display to mainscreen something
gui = ParkingBuildingGUI()
gui.main_section()
my_time()
root.mainloop()
