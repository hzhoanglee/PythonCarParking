import customtkinter as ttk
import tkinter as tk
from tkinter import ttk as ttkz
from tkinter import *
from PIL import Image
from time import strftime
from ManSys import ManagementSystem
from tkinter import messagebox as mbox
from utils.connect import mydb
from login_verification import LoginVerification


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


class ParkingBuildingGUI:
    def __init__(self, ms):
        self.ms = ms
        self.building_settings = self.ms.get_settings()
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
        main = ttk.CTkFrame(master=template.root, width=500,
                            height=1300)
        main.place(x=233, y=100)

        # Customize the floor buttons
        s = ttkz.Style()
        s.theme_use('default')
        s.configure('TNotebook.Tab', font=("clam", 12, "bold"), width=15, height=100, background="#E0E0E0")
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
        slot = self.ms.get_slot_by_code(slot_code)
        if slot.is_available():
            self.open_check_in(slot_code)
        else:
            self.open_check_out(slot_code)

    def open_check_in(self, slot_code="Auto"):
        # Creating the screen
        new = ttk.CTkToplevel(template.root)
        new.resizable(True, True)
        new.title("Car Check In Window")
        new.config(background=template.mainScreenColor)
        x = template.root.winfo_x()
        y = template.root.winfo_y()
        new.geometry("+%d+%d" % (x + 300, y + 150))
        new.geometry('500x450')

        # form
        label = ttk.CTkLabel(master=new,
                             text="Car Check In",
                             text_color=template.grayColor,
                             font=('', 20, 'bold'),
                             fg_color=template.mainScreenColor, ).place(x=100, y=90)

        driverName = ttk.CTkEntry(master=new,
                                  width=300,
                                  height=40,
                                  placeholder_text='Driver Name',
                                  bg_color=template.mainScreenColor)
        driverName.place(x=100, y=140)

        licensePlate = ttk.CTkEntry(master=new,
                                    width=300,
                                    height=40,
                                    placeholder_text='License plate',
                                    bg_color=template.frameColor
                                    )
        licensePlate.place(x=100, y=195)

        # Getting slot codes
        slot_codes = ['Auto']
        lst = self.ms.get_unused_slots()
        for slot in lst:
            slot_codes.append(str(slot.get_slot_code()))

        # Dropdown box
        dropdown = ttk.CTkOptionMenu(master=new,
                                     height=40,
                                     values=slot_codes,
                                     button_color=template.mainColor,
                                     fg_color=template.mainColor,
                                     button_hover_color=template.hoverColor,
                                     dropdown_hover_color=template.hoverColor
                                     )
        dropdown.set(slot_code)
        dropdown.place(x=100, y=250)

        def submit():
            # Check if all fields are filled out
            if driverName.get() and licensePlate.get() and dropdown.get():
                # Check if dropdown menu has a value selected
                if dropdown.get() != "Auto":
                    # Add car
                    self.ms.checkin(driverName.get(), licensePlate.get(), dropdown.get())
                    # Show success message
                    mbox.showinfo("Success", "A car has been added.")
                    # Close the Toplevel window
                    self.main_section()
                    new.destroy()
                    # Reload the table

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
                                     fg_color=template.mainColor,
                                     font=("", 15, 'bold'),
                                     text_color='white',
                                     cursor="hand2",
                                     hover_color='#ccccff', command=lambda: submit())
        submitButton.place(x=100, y=320)

        # Keep the toplevel window in front of the root window
        new.wm_transient(template.root)
        new.mainloop()

    def open_check_out(self, slot_code):
        # Creating the screen
        new = ttk.CTkToplevel(template.root)
        new.resizable(True, True)
        new.title("Car Check Out Window")
        new.config(background=template.mainScreenColor)
        x = template.root.winfo_x()
        y = template.root.winfo_y()
        new.geometry("+%d+%d" % (x + 300, y + 150))
        new.geometry('500x450')

        # form
        label = ttk.CTkLabel(master=new,
                             text="Car Check Out",
                             text_color=template.grayColor,
                             font=('', 20, 'bold'),
                             fg_color=template.mainScreenColor, ).place(x=100, y=90)

        # Get Car info
        slot = self.ms.get_slot_by_code(slot_code)
        car = slot.get_car()
        driverName = car.get_driver_name()
        licensePlate = car.get_license_plate()

        # Display car info
        ttk.CTkLabel(master=new,
                     text="Driver Name: " + driverName,
                     text_color=template.grayColor,
                     font=('', 15, 'bold'),
                     fg_color=template.mainScreenColor, ).place(x=100, y=140)
        ttk.CTkLabel(master=new,
                     text="License Plate: " + licensePlate,
                     text_color=template.grayColor,
                     font=('', 15, 'bold'),
                     fg_color=template.mainScreenColor, ).place(x=100, y=195)

        # Getting slot codes
        slot_codes = [slot_code]

        # Dropdown box
        dropdown = ttk.CTkOptionMenu(master=new,
                                     height=40,
                                     values=slot_codes,
                                     button_color=template.mainColor,
                                     fg_color=template.mainColor,
                                     button_hover_color=template.hoverColor,
                                     dropdown_hover_color=template.hoverColor
                                     )
        dropdown.set(slot_code)
        dropdown.place(x=100, y=250)

        def checkout_submit():
            if dropdown.get():
                if dropdown.get() != "Auto":
                    price = self.ms.checkout(dropdown.get())
                    check_out_text = "Check Out success. Total price: " + str(price)
                    mbox.showinfo("Success", check_out_text)
                    self.main_section()
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
                                     fg_color=template.mainColor,
                                     font=("", 15, 'bold'),
                                     text_color='white',
                                     cursor="hand2",
                                     hover_color='#ccccff', command=lambda: checkout_submit())
        submitButton.place(x=100, y=320)

        # Keep the toplevel window in front of the root window
        new.wm_transient(template.root)
        new.mainloop()


class Builder:
    def __init__(self, ms):
        self.root = None
        self.ms = ms
        # Setting the theme for the main window
        self.manageButton = None
        self.logout_text = None
        self.manageImage = None
        self.l1 = None
        self.logo = None
        self.carButton = None
        self.name = None
        self.carImage = None
        self.logoImage = None
        self.sideBar = None
        self.header = None
        self.time_string = None
        ttk.set_appearance_mode('light')
        self.mainColor = "#8685ef"
        self.sideColor = "#faf8ff"
        self.mainScreenColor = '#f2ecff'
        self.frameColor = '#e9e1ff'
        self.grayColor = '#737373'
        self.hoverColor = '#ccccff'
        self.login = LoginVerification()
        self.build_root()

    def build_root(self):
        # Setting the main window
        self.root = ttk.CTk()
        self.root.geometry('970x700')
        self.root.resizable(True, True)
        self.root.title("Vịt Quay Parking System")
        self.root.config(background='#f2ecff')

    def kill_root(self):
        self.root.destroy()
        self.build_root()
        self.login_screen()

    def login_screen(self):
        # Creating the screen
        self.login_window = ttk.CTk()
        self.login_window.geometry('500x300')
        self.login_window.resizable(True, True)
        self.login_window.title("Vịt Quay Parking System")
        self.login_window.config(background='#f2ecff')

        # Creating the login form
        self.l1 = ttk.CTkLabel(master=self.login_window,
                               text="Vịt Quay Parking System",
                               text_color=self.grayColor,
                               font=('', 30, 'bold'),
                               fg_color=self.mainScreenColor, ).place(x=80, y=50)

        # Password label
        passwordLabel = ttk.CTkLabel(master=self.login_window,
                                     text="Password",
                                     text_color=self.grayColor,
                                     font=('', 15, 'bold'),
                                     fg_color=self.mainScreenColor, ).place(x=120, y=130)

        # Password entry
        passwordEntry = ttk.CTkEntry(master=self.login_window,
                                     width=200,
                                     fg_color=self.mainColor,
                                     font=('', 15, 'bold'),
                                     border_color=self.mainColor,
                                     show="*")
        passwordEntry.place(x=120, y=160)

        # Login button
        loginButton = ttk.CTkButton(master=self.login_window,
                                    height=40,
                                    text="Login",
                                    fg_color=self.mainColor,
                                    font=("", 15, 'bold'),
                                    text_color='white',
                                    cursor="hand2",
                                    hover_color='#ccccff', command=lambda: self.check_login(passwordEntry.get()))
        loginButton.place(x=120, y=200)

        # Keep the toplevel window in front of the root window
        self.login_window.mainloop()

    def check_login(self, password):
        if self.login.verify_password(password):
            self.login_window.destroy()
            self.run()
        else:
            mbox.showerror("Error", "Wrong password")

    def build(self):
        # Creating the header
        self.header = ttk.CTkFrame(self.root,
                                   width=1070,
                                   height=60,
                                   fg_color="#8685ef")
        self.header.place(x=201, y=0)

        # Log out button
        self.logout_text = ttk.CTkButton(self.header,
                                         text="Logout",
                                         font=("", 13, "bold"),
                                         fg_color='white',
                                         cursor='hand2',
                                         text_color=self.mainColor,
                                         hover_color='#ccccff', command=lambda: self.kill_root())
        self.logout_text.place(x=588, y=15)

        # ====================================
        # =============END OF HEADER==========
        # ====================================

        # ===============================================
        # =====================SIDEBAR===================
        # ===============================================

        # Sidebar
        self.sideBar = ttk.CTkFrame(master=self.root, width=200,
                                    height=1300,
                                    fg_color="#faf8ff")
        self.sideBar.place(x=0, y=0)

        # Logo
        self.logoImage = ttk.CTkImage(light_image=Image.open("images/icon.png"),
                                      size=(100, 100))
        self.logo = ttk.CTkLabel(self.sideBar,
                                 text='',
                                 image=self.logoImage)
        self.logo.place(x=50, y=80)

        # Name of the person
        self.name = ttk.CTkLabel(master=self.sideBar,
                                 text="ADMIN",
                                 font=("", 15, "bold"),
                                 text_color="#737373")
        self.name.place(x=75, y=180)
        self.name.place(x=75, y=190)

        # ===============================================
        # =====================BUTTONS===================
        # ===============================================

        # Car check in
        self.carImage = ttk.CTkImage(light_image=Image.open('images/car.png'),
                                     size=(25, 25))

        self.carButton = ttk.CTkButton(master=self.sideBar,
                                       image=self.carImage,
                                       text="Car check-in",
                                       width=200,
                                       height=50,
                                       compound='left',
                                       fg_color='transparent',
                                       text_color=self.mainColor,
                                       font=('', 15, 'bold'),
                                       cursor="hand2",
                                       anchor='center',
                                       hover_color='#ccccff',
                                       command=lambda: self.open_check_in(),
                                       ).place(x=0, y=250)

        # Manage vehicle

        self.manageImage = ttk.CTkImage(light_image=Image.open('images/manage.png'),
                                        size=(20, 20))
        self.manageButton = ttk.CTkButton(master=self.sideBar,
                                          image=self.manageImage,
                                          text="Manage vehicle",
                                          width=200,
                                          height=50,
                                          compound='left',
                                          fg_color='transparent',
                                          text_color=self.mainColor,
                                          font=('', 15, 'bold'),
                                          cursor="hand2",
                                          anchor='center',
                                          hover_color='#ccccff',
                                          command=lambda: self.open_manage()
                                          ).place(x=0, y=300)

        # Settings
        self.settingsImage = ttk.CTkImage(light_image=Image.open('images/settings.png'),
                                          size=(25, 25))

        self.settingsButton = ttk.CTkButton(master=self.sideBar,
                                            image=self.settingsImage,
                                            text="Settings",
                                            width=200,
                                            height=50,
                                            compound='left',
                                            fg_color='transparent',
                                            text_color=self.mainColor,
                                            font=('', 15, 'bold'),
                                            cursor="hand2",
                                            anchor='center',
                                            hover_color='#ccccff',
                                            command=lambda: self.open_settings(),
                                            ).place(x=0, y=350)

        # ===============================================
        # =====================END OF BUTTONS============
        # ===============================================

        # ===============================================
        # =====================TIME======================
        # ===============================================

        self.l1 = ttk.CTkLabel(master=self.sideBar, font=('', 15, 'bold'), text_color=self.grayColor)
        self.l1.place(x=50, y=400)
        self.l1.place(x=50, y=450)

        # ===============================================
        # =====================END OF TIME===============
        # ===============================================

        # ======================================================
        # =====================END OF SIDEBAR===================
        # ======================================================

        # ======================================================
        # =====================MAIN SCREEN======================
        # ======================================================

    def my_time(self):
        self.time_string = strftime('%H:%M:%S %p \n %A \n %x')
        self.l1.configure(text=self.time_string)
        self.l1.after(1000, self.my_time)  # time delay of 1000 milliseconds

    def open_manage(self):
        # Creating the screen
        new = ttk.CTkToplevel(self.root)
        new.resizable(True, True)
        new.title("Manage Car Window")
        new.config(background=self.mainScreenColor)
        new.geometry('600x520')

        # Connect to DB
        new.dbconnection = mydb.cursor()
        new.dbconnection.execute("SELECT * FROM check_ins")

        # CSS
        style = ttkz.Style()
        style.configure("Treeview",
                        background="#f9f9f9",
                        foreground="#6f727a",
                        fieldbackground="#ddeaef",
                        rowheight=60,
                        borderwidth=5,
                        border="#6f727a",
                        font=(None, 12))

        style.configure("Treeview.Heading",
                        background="#d7d2ea",
                        rowheight=80,
                        foreground="#6f727a",
                        font=("Bold", 14))

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
        used_slot = self.ms.get_used_slot_count()
        lab1 = Label(new, font=("#6f727a", 14, "bold"), width=15,
                     height=2,
                     text="Occupied slots : ")
        lab1.place(x=60, y=670)
        lab2 = Label(new, font=("#6f727a", 16, "bold"),
                     width=15,
                     height=2,
                     text=used_slot)
        lab2.place(x=250, y=670)

        # Available slots
        avail_slot = self.ms.get_available_slot_count()
        lab3 = Label(new, font=("#6f727a", 14, "bold"), width=15,
                     height=2,
                     text="Available slots : ")
        lab3.place(x=460, y=670)
        lab4 = Label(new, font=("#6f727a", 16, "bold"),
                     width=15,
                     height=2,
                     text=avail_slot)
        lab4.place(x=650, y=670)

        new.wm_transient(self.root)
        new.mainloop()

    def open_settings(self):
        # Creating the screen
        new = ttk.CTkToplevel(self.root)
        new.resizable(True, True)
        new.title("Settings")
        new.config(background=self.mainScreenColor)
        new.geometry('400x400')

        # Get settings
        settings = self.ms.get_settings()
        # Show current settings
        current_settings_label = tk.Label(new, text="Current Settings ",
                                          font=('', 15, 'bold'),
                                          foreground=self.grayColor)
        current_settings_label.place(x=30, y=80)

        # Using label to show text
        current_x_val = tk.Label(new, text="X value             " + str(settings.get_X_VALUE()),
                                 font=('', 15, 'bold'),
                                 foreground=self.mainColor)
        current_x_val.place(x=300, y=40)
        current_y_val = tk.Label(new, text="Y value             " + str(settings.get_Y_VALUE()), font=('', 15, 'bold'),
                                 foreground=self.mainColor)
        current_y_val.place(x=300, y=80)
        current_z_val = tk.Label(new, text="Z value             " + str(settings.get_Z_VALUE()), font=('', 15, 'bold'),
                                 foreground=self.mainColor)
        current_z_val.place(x=300, y=120)
        current_parking_fee = tk.Label(new, text="Parking fee   " + str(settings.get_parking_fee()),
                                       font=('', 15, 'bold'), foreground=self.mainColor)
        current_parking_fee.place(x=300, y=160)

        # Edit settings
        divider = tk.Label(new, text="-------------------------------------------------------------",
                           font=('', 18, 'bold'), foreground=self.mainColor)
        divider.place(x=50, y=220)
        edit_settings_label = tk.Label(new, text="Edit Settings ", font=('', 15, 'bold'), foreground=self.grayColor)
        edit_settings_label.place(x=30, y=310)

        # Using label to show text
        # X
        x_val_label = tk.Label(new, text="New X value ", font=('', 15, 'bold'), foreground=self.mainColor)
        x_val_label.place(x=250, y=270)
        x_val_entry = tk.Entry(new, background=self.mainScreenColor, foreground=self.grayColor)
        x_val_entry.pack(side=BOTTOM, ipadx=30, ipady=20)
        x_val_entry.place(x=400, y=275)

        # Y
        y_val_label = tk.Label(new, text="New Y value ", font=('', 15, 'bold'), foreground=self.mainColor)
        y_val_label.place(x=250, y=320)
        y_val_entry = tk.Entry(new, background=self.mainScreenColor, foreground=self.grayColor)
        y_val_entry.pack(side=BOTTOM, ipadx=30, ipady=20)
        y_val_entry.place(x=400, y=325)

        # Z
        z_val_label = tk.Label(new, text="New Z value ", font=('', 15, 'bold'), foreground=self.mainColor)
        z_val_label.place(x=250, y=370)
        z_val_entry = tk.Entry(new, background=self.mainScreenColor, foreground=self.grayColor)
        z_val_entry.pack(side=BOTTOM, ipadx=30, ipady=20)
        z_val_entry.place(x=400, y=375)

        # Fees
        parking_fee_label = tk.Label(new, text="New fee ", font=('', 15, 'bold'), foreground=self.mainColor)
        parking_fee_label.place(x=250, y=420)
        parking_fee_entry = tk.Entry(new, background=self.mainScreenColor, foreground=self.grayColor)
        parking_fee_entry.pack(side=BOTTOM, ipadx=30, ipady=20)
        parking_fee_entry.place(x=400, y=425)

        # Password
        password_label = tk.Label(new, text="New password ", font=('', 15, 'bold'), foreground=self.mainColor)
        password_label.place(x=250, y=470)
        password_entry = tk.Entry(new, background=self.mainScreenColor, foreground=self.grayColor)
        password_entry.pack(side=BOTTOM, ipadx=30, ipady=20)
        password_entry.place(x=400, y=475)
        # using button to upload settings
        upload_button = tk.Button(new,
                                  text="Upload",
                                  background="white",
                                  foreground=self.mainColor,
                                  font=('', 13, "bold"),
                                  height=1,
                                  width=6,
                                  cursor='hand2',
                                  command=lambda: self.upload_settings(x_val_entry,
                                                                       y_val_entry,
                                                                       z_val_entry,
                                                                       password_entry,
                                                                       parking_fee_entry))
        upload_button.place(x=30, y=440)

    def upload_settings(self, x_val_ent, y_val_ent, z_val_ent, password_ent, parking_fee_ent):
        x_val = x_val_ent.get()
        y_val = y_val_ent.get()
        z_val = z_val_ent.get()
        password = password_ent.get()
        parking_fee = parking_fee_ent.get()
        self.ms.edit_settings(x_val, y_val, z_val, password, parking_fee)
        x_val_ent.delete(0, 'end')
        y_val_ent.delete(0, 'end')
        z_val_ent.delete(0, 'end')
        password_ent.delete(0, 'end')
        parking_fee_ent.delete(0, 'end')
        self.refresh()

    def refresh(self):
        self.root.destroy()
        self.__init__()
        self.root.main_loop()

    def run(self):
        self.ms.setup_parking_lot()
        self.build()
        self.my_time()
        gui = ParkingBuildingGUI(self.ms)
        gui.main_section()
        self.root.mainloop()


if __name__ == '__main__':
    ms = ManagementSystem()
    template = Builder(ms)

    template.login_screen()
