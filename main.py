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

    def daily_report(self):
        # daily fee
        daily_history = self.ms.get_daily_report()
        daily_fee_total = self.ms.calculate_total_income(daily_history)
        # add text to (x=500, y=15)
        daily_fee_lbl = ttk.CTkLabel(template.header,
                                     text="Report Total Fee: " + str(daily_fee_total),
                                     font=("", 13, "bold"),
                                     fg_color=template.mainColor,
                                     text_color='white')
        daily_fee_lbl.place(x=20, y=10)

        max_slot = self.ms.get_max_slot_count()
        used_slot = self.ms.io_car.get_used_slot_count()
        available_slot = self.ms.io_car.get_available_slot_count()

        # add text to (x=500, y=15)
        slot_lbl = ttk.CTkLabel(template.header,
                                text="Max Slot: " + str(max_slot)
                                     + " | Used Slot: " + str(used_slot)
                                     + " | Available Slot: " + str(available_slot),
                                font=("", 13, "bold"),
                                fg_color=template.mainColor,
                                text_color='white')
        slot_lbl.place(x=20, y=30)

    def main_section(self):
        # Print main window in the right of sidebar
        main = ttk.CTkFrame(master=template.root, width=500,
                            height=1300)
        main.place(x=233, y=100)

        # Customize the floor buttons
        s = ttkz.Style()
        s.configure("TNotebook", foreground=template.mainScreenColor, background=template.mainScreenColor, borderwidth=0)
        s.configure("TNotebook.Tab", font=(template.mainColor, 12, "bold"), width=15, height=100, background=template.mainScreenColor,
                    foreground=template.mainColor,
                    lightcolor=template.mainColor, borderwidth=0)
        s.configure("TFrame", background=template.mainScreenColor, foreground="white", borderwidth=0)
        self.daily_report()
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
        # self.build_root()

    def build_root(self):
        # Setting the main window
        self.root = ttk.CTk()
        self.root.geometry('970x700')
        self.root.resizable(True, True)
        self.root.title(self.ms.get_name())
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
        self.login_window.title(self.ms.get_name())
        self.login_window.config(background='#f2ecff')

        # Creating the login form
        self.l1 = ttk.CTkLabel(master=self.login_window,
                               text=self.ms.get_name(),
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

        self.login_window.mainloop()

    def check_login(self, password):
        if self.login.verify_password(password):
            self.login_window.destroy()
            self.build_root()
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
        # self.logout_text = ttk.CTkButton(self.header,
        #                                  text="Logout",
        #                                  font=("", 13, "bold"),
        #                                  fg_color='white',
        #                                  cursor='hand2',
        #                                  text_color=self.mainColor,
        #                                  hover_color='#ccccff', command=lambda: self.kill_root())
        # self.logout_text.place(x=588, y=15)

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
                                       command=lambda: self.gui.open_check_in(),
                                       ).place(x=0, y=250)

        # Manage vehicle

        self.manageImage = ttk.CTkImage(light_image=Image.open('images/manage.png'),
                                        size=(20, 20))
        self.manageButton = ttk.CTkButton(master=self.sideBar,
                                          image=self.manageImage,
                                          text="Car Logs",
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

        # About
        self.aboutImage = ttk.CTkImage(light_image=Image.open('images/about.png'),
                                       size=(25, 25))
        self.aboutButton = ttk.CTkButton(master=self.sideBar,
                                         image=self.aboutImage,
                                         text="About",
                                         width=200,
                                         height=50,
                                         compound='left',
                                         fg_color='transparent',
                                         text_color=self.mainColor,
                                         font=('', 15, 'bold'),
                                         cursor="hand2",
                                         anchor='center',
                                         hover_color='#ccccff',
                                         command=lambda: self.open_about(),
                                         ).place(x=0, y=400)

        # ===============================================
        # =====================END OF BUTTONS============
        # ===============================================

        # ===============================================
        # =====================TIME======================
        # ===============================================

        self.l1 = ttk.CTkLabel(master=self.sideBar, font=('', 15, 'bold'), text_color=self.grayColor)
        self.l1.place(x=50, y=400)
        self.l1.place(x=50, y=500)

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
        self.time_string = strftime('%H:%M:%S %p \n %A \n %x\n Version: 1.4')
        self.l1.configure(text=self.time_string)
        self.l1.after(1000, self.my_time)

    def open_manage(self):
        # Creating the screen
        new = ttk.CTkToplevel(self.root)
        new.resizable(True, True)
        new.title("Manage Car Window")
        new.config(background=self.mainScreenColor)
        new.geometry('1280x600')

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

    def open_about(self):
        new = ttk.CTkToplevel(template.root)
        new.resizable(True, True)
        new.title("About")
        new.config(background=template.mainScreenColor)
        x = template.root.winfo_x()
        y = template.root.winfo_y()
        new.geometry("+%d+%d" % (x + 300, y + 150))
        new.geometry('500x500')

        # using label to show text
        devs_label = ttk.CTkLabel(master=new, text_color=template.mainColor, fg_color=template.mainScreenColor,
                                  text="Developers:", font=("", 24, 'bold'))
        devs_label.pack(pady=10)

        about_label_devs = ttk.CTkLabel(master=new, text_color=template.grayColor, fg_color=template.mainScreenColor,
                                        font=("", 16),
                                        text="IO/Core Functions: Le Tuan Huy(BI12-195) "
                                             "\n\nUI/FE: Nguyen Minh Hoang(BI12-172)"
                                             "\n\nCore/Planner: Le Minh Hoang(BI12-167)"
                                             "\n\nTesting: Nguyen The Hoang(BI12-171)"
                                             "\n\nUI/Report: Nguyen Vu Viet Hoang(BI12-173)")
        about_label_devs.pack()

        divider = ttk.CTkLabel(master=new, text_color=template.grayColor, fg_color=template.mainScreenColor,
                               text="----------------------------------------")
        divider.pack()
        # Contact
        contact_label = ttk.CTkLabel(master=new, text_color=template.mainColor, fg_color=template.mainScreenColor,
                                     text="Contacts:", font=("", 24, 'bold'))
        contact_label.pack(pady=10)

        about_label_contact = ttk.CTkLabel(master=new, text_color=template.grayColor, fg_color=template.mainScreenColor,
                                           font=("", 16),
                                           text="huylt.bi12-195@st.usth.edu.vn"
                                                "\n\nhoangnm.bi12-172@st.usth.edu.vn"
                                                "\n\nhoanglm.bi12-167@st.usth.edu.vn - https://hzme.net"
                                                "\n\nhoangnt.bi12-171@st.usth.edu.vn"
                                                "\n\nhoangnvv.bi12-173@st.usth.edu.vn")
        about_label_contact.pack()

        divider = ttk.CTkLabel(master=new, text_color=template.grayColor, fg_color=template.mainScreenColor,
                               text="----------------------------------------")
        divider.pack()

        new.wm_transient(template.root)
        new.mainloop()

    def open_settings(self):
        # Creating the screen
        new = ttk.CTkToplevel(template.root)
        new.resizable(True, True)
        new.title("Settings")
        new.config(background=template.mainScreenColor)
        x = template.root.winfo_x()
        y = template.root.winfo_y()
        new.geometry("+%d+%d" % (x + 300, y + 150))
        new.geometry('800x600')

        # Get settings
        settings = self.ms.get_settings()

        # Using label to show text
        label = ttk.CTkLabel(master=new,
                             text="System Settings",
                             text_color=template.grayColor,
                             font=('', 20, 'bold'),
                             fg_color=template.mainScreenColor).place(x=100, y=40)

        label_x = ttk.CTkLabel(master=new,
                               text="X value:",
                               text_color=template.grayColor,
                               font=('', 18),
                               fg_color=template.mainScreenColor)
        label_x.place(x=100, y=150)
        x_val_change = ttk.CTkEntry(master=new,
                                    width=300,
                                    height=40,
                                    placeholder_text='Value for X',
                                    bg_color=template.mainScreenColor)
        x_val_change.place(x=200, y=140)
        x_val_change.insert("0", str(settings.get_X_VALUE()))

        label_y = ttk.CTkLabel(master=new,
                               text="Y value:",
                               text_color=template.grayColor,
                               font=('', 18),
                               fg_color=template.mainScreenColor)
        label_y.place(x=100, y=200)
        y_val_change = ttk.CTkEntry(master=new,
                                    width=300,
                                    height=40,
                                    placeholder_text='Value for Y',
                                    bg_color=template.mainScreenColor)
        y_val_change.setvar(str(settings.get_Y_VALUE()))
        y_val_change.place(x=200, y=190)
        y_val_change.insert("0", str(settings.get_Y_VALUE()))

        label_z = ttk.CTkLabel(master=new,
                               text="Z value:",
                               text_color=template.grayColor,
                               font=('', 18),
                               fg_color=template.mainScreenColor)
        label_z.place(x=100, y=250)
        z_val_change = ttk.CTkEntry(master=new,
                                    width=300,
                                    height=40,
                                    placeholder_text='Value for Z',
                                    bg_color=template.mainScreenColor)
        z_val_change.place(x=200, y=240)
        z_val_change.insert("0", str(settings.get_Z_VALUE()))

        label_fee = ttk.CTkLabel(master=new,
                                 text="Fee:",
                                 text_color=template.grayColor,
                                 font=('', 18),
                                 fg_color=template.mainScreenColor)
        label_fee.place(x=100, y=300)
        fee_val_change = ttk.CTkEntry(master=new,
                                      width=300,
                                      height=40,
                                      placeholder_text='Fee Setting',
                                      bg_color=template.mainScreenColor)
        fee_val_change.place(x=200, y=290)
        fee_val_change.insert("0", str(settings.get_parking_fee()))

        label_name = ttk.CTkLabel(master=new,
                                  text="Name:",
                                  text_color=template.grayColor,
                                  font=('', 18),
                                  fg_color=template.mainScreenColor)
        label_name.place(x=100, y=350)
        label_val_change = ttk.CTkEntry(master=new,
                                        width=300,
                                        height=40,
                                        placeholder_text='Name',
                                        bg_color=template.mainScreenColor)
        label_val_change.place(x=200, y=340)
        label_val_change.insert("0", str(settings.get_name()))

        submitButton = ttk.CTkButton(master=new,
                                     height=40,
                                     text="Save Settings",
                                     fg_color=template.mainColor,
                                     font=("", 15, 'bold'),
                                     text_color='white',
                                     cursor="hand2",
                                     hover_color='#ccccff', command=lambda: self.upload_settings(x_val_change.get(),
                                                                                                 y_val_change.get(),
                                                                                                 z_val_change.get(),
                                                                                                 fee_val_change.get(),
                                                                                                 label_val_change.get()))

        submitButton.place(x=150, y=440)
        new.wm_transient(template.root)
        new.mainloop()

    def upload_settings(self, x_val, y_val, z_val, parking_fee_val, name):
        password = None
        self.ms.edit_settings(x_val, y_val, z_val, password, parking_fee_val)
        self.ms.change_name(name)
        self.refresh()

    def refresh(self):
        # self.root.destroy()
        # self.__init__(self.ms)
        # self.build()
        # self.my_time()
        # self.gui = ParkingBuildingGUI(self.ms)
        # self.gui.main_section()
        # self.root.main_loop()
        self.root.destroy()
        self.__init__(self.ms)
        self.build_root()
        self.run()

    def run(self):
        self.ms.setup_parking_lot()
        self.build()
        self.my_time()
        self.gui = ParkingBuildingGUI(self.ms)
        self.gui.main_section()
        self.root.mainloop()


if __name__ == '__main__':
    ms = ManagementSystem()
    template = Builder(ms)

    template.login_screen()
