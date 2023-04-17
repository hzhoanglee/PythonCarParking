import tkinter as tk
from tkinter import ttk
from ManSys import ManagementSystem
from login_verification import LoginVerification

#ms = ManagementSystem()
#ms.setup_parking_lot()


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
    def __init__(self, tk_window, ms):
        self.window = tk_window
        self.window.title("Parking Building")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.ms = ms
        self.building_settings = self.ms.get_settings()
        floor_count = int(self.building_settings.get_Z_VALUE())
        self.building_floors = []
        for i in range(floor_count):
            floor_code = f"F{i}"
            floor_slots = []
            for slot in self.ms.get_slot_list():
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

    def main_window(self):
        # main window with tabs each tab is a floor
        window = tk.Toplevel(self.window)
        tab_control = ttk.Notebook(window)
        for floor in self.building_floors:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=floor.get_floor_code())
            tab_control.pack(expand=1, fill="both")
            self.floor_window(tab, floor)
        self.window.mainloop()

    def floor_window(self, tab, floor, slot_button_list=None):
        # create a button for each slot add to list
        if slot_button_list is None:
            slot_button_list = []

        for slot in floor.get_floor_slots():
            slot_button = tk.Button(tab, text=slot.get_slot_code(),
                                    command=lambda slot_code=slot.get_slot_code(): self.slot_window(slot_code))
            slot_button_list.append(slot_button)

        # use grid to place buttons in a table
        for i in range(len(slot_button_list)):
            slot_code = slot_button_list[i].cget("text")
            row = i // len(self.x_list)
            col = i % len(self.x_list)
            slot_button_list[i].grid(row=row, column=col)
            if self.ms.get_slot_by_code(slot_code).is_available():
                slot_button_list[i].config(bg="green")
            else:
                slot_button_list[i].config(bg="red")
    def slot_window(self, slot_code):
        # create a window for each slot
        self.slot_window_tk = tk.Toplevel(self.window)
        self.slot_window_tk.title(slot_code)
        self.slot_window_tk.geometry("400x300")
        self.slot_window_tk.resizable(True, True)
        self.slot_window_tk.grab_set()
        self.slot_window_tk.focus_set()
        self.slot_window_tk.transient(self.window)

        slot = self.ms.get_slot_by_code(slot_code)
        if slot.is_available():
            #insert label for slot status: Status: Available
            slot_status_label = tk.Label(self.slot_window_tk, text="Status: Available")
            slot_status_label.pack()
            slot_button = tk.Button(self.slot_window_tk, text="Check In", command=lambda: self.checkin_window(slot_code))
            slot_button.pack()
        else:
            # insert label for slot status: Status: Occupied
            # insert label for car plate: Car Plate: xxx
            # insert label for driver name: Driver Name: xxx

            slot_status_label = tk.Label(self.slot_window_tk, text="Status: Occupied")
            slot_status_label.pack()
            car_plate_label = tk.Label(self.slot_window_tk, text="Car Plate: " + slot.get_car().get_license_plate())
            car_plate_label.pack()
            driver_name_label = tk.Label(self.slot_window_tk, text="Driver Name: " + slot.get_car().get_driver_name())
            driver_name_label.pack()
            slot_button = tk.Button(self.slot_window_tk, text="Check Out", command=lambda: self.checkout_window(slot_code))
            slot_button.pack()
        self.slot_window_tk.protocol("WM_DELETE_WINDOW", lambda: self.slot_window_tk.destroy())

    def checkin_window(self, slot_code):
        # create a window for checkin
        checkin_window = tk.Toplevel(self.window)
        checkin_window.title("Check In")
        checkin_window.geometry("400x300")
        checkin_window.resizable(True, True)
        checkin_window.grab_set()
        checkin_window.focus_set()
        checkin_window.transient(self.window)

        # create a label for car plate
        car_plate_label = tk.Label(checkin_window, text="Car Plate")
        car_plate_label.pack()

        # create a entry for car plate
        car_plate_entry = tk.Entry(checkin_window)
        car_plate_entry.pack()

        # driver name
        driver_name_label = tk.Label(checkin_window, text="Driver Name")
        driver_name_label.pack()

        # driver name entry
        driver_name_entry = tk.Entry(checkin_window)
        driver_name_entry.pack()

        # create a button for checkin
        checkin_button = tk.Button(checkin_window,
                                   text="Check In",
                                   command=lambda: self.check_in_button(slot_code, driver_name_entry, car_plate_entry, checkin_window))
        checkin_button.pack()


        self.slot_window_tk.destroy()
        checkin_window.protocol("WM_DELETE_WINDOW", lambda: checkin_window.destroy())

    def check_in_button(self, slot_code, driver_name_entry, car_plate_entry, tk_window):
        # create a button for checkout
        driver_name = driver_name_entry.get()
        car_plate = car_plate_entry.get()
        self.ms.checkin(driver_name, car_plate, slot_code)
        driver_name_entry.delete(0, tk.END)
        car_plate_entry.delete(0, tk.END)
        # label for insert after checkin
        checkin_label = tk.Label(tk_window, text="checkin successfully")
        checkin_label.pack()
        #tk_window.destroy()

    def checkout_window(self, slot_code):
        # create a window for checkout
        checkout_window = tk.Toplevel(self.window)
        checkout_window.title("Check Out")
        checkout_window.geometry("400x300")
        checkout_window.resizable(True, True)
        checkout_window.grab_set()
        checkout_window.focus_set()
        checkout_window.transient(self.window)

        # create a label "Are you sure to check out?"
        checkout_label = tk.Label(checkout_window, text="Are you sure to check out?")
        checkout_label.pack()
        # create a button for checkout
        checkout_button = tk.Button(checkout_window,
                                    text="Check Out",
                                    command=lambda: self.check_out_button(slot_code, checkout_window))
        checkout_button.pack()
        self.slot_window_tk.destroy()
        checkout_window.protocol("WM_DELETE_WINDOW", lambda: checkout_window.destroy())

    def check_out_button(self, slot_code, tk_window):
        # create a button for checkout
        fee = self.ms.checkout(slot_code)
        # label for insert after checkout
        checkout_label = tk.Label(tk_window, text="checkout successfully")
        checkout_label.pack()
        # insert label for fee: Fee: xxx
        fee_label = tk.Label(tk_window, text="Fee: " + str(fee))
        fee_label.pack()
        #refresh the dashboard
        #tk_window.destroy()

class Dashboard:
    def __init__(self):
        self.ms = ManagementSystem()
        self.ms.setup_parking_lot()
        self.dashboard_window = tk.Tk()
        self.ParkingBuildingGUI = ParkingBuildingGUI(self.dashboard_window, self.ms)
        self.dashboard_window.title("Parking System (Emergency GUI)")
        # dashboard window must bigger than ParkingBuildingGUI
        self.dashboard_window.geometry("1000x800")
        self.dashboard_window.resizable(True, True)

    def main_window(self):
        # using notebook to create tabs, each tab is a window to show different content
        #1. is the parking building map (ParkingBuildingGUI)
        #2. is the about and help content, contact us (N/a)

        tab_control = ttk.Notebook(self.dashboard_window)

        #tab1: parking building tab
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text="Parking Building")
        tab_control.pack(expand=1, fill="both")
        notebook_tab1 = ttk.Notebook(tab1)
        notebook_tab1.pack(expand=1, fill="both")
        #get floor list from ParkingBuildingGUI
        for floor in self.ParkingBuildingGUI.building_floors:
            tab = ttk.Frame(notebook_tab1)
            notebook_tab1.add(tab, text=floor.get_floor_code())
            self.ParkingBuildingGUI.floor_window(tab, floor)

        #add refresh button
        refresh_button = tk.Button(tab1, text="Refresh", command=self.refresh)
        refresh_button.pack()

        #tab2: general info tab
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text="General Info")
        tab_control.pack(expand=1, fill="both")
        # get max slot number
        max_slot_number = self.ms.get_max_slot_count()
        # get used slot number
        used_slot_number = self.ms.io_car.get_used_slot_count()
        # get free slot number
        free_slot_number = self.ms.io_car.get_available_slot_count()

        # using label to show text
        general_info_label = tk.Label(tab2, text="Max Slot Number: " + str(max_slot_number)
                                        + "\nUsed Slot Number: " + str(used_slot_number)
                                        + "\nFree Slot Number: " + str(free_slot_number))
        general_info_label.pack()


        #tab3: setting tab(show, edit setting)
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text="Settings")
        tab_control.pack(expand=1, fill="both")
        #get settings
        settings = self.ms.get_settings()
        #Show current settings
        current_settings_label = tk.Label(tab3, text="Current Settings: ")
        current_settings_label.pack()
        #using label to show text
        current_x_val = tk.Label(tab3, text="x_val: " + str(settings.get_X_VALUE()))
        current_x_val.pack()
        current_y_val = tk.Label(tab3, text="y_val: " + str(settings.get_Y_VALUE()))
        current_y_val.pack()
        current_z_val = tk.Label(tab3, text="z_val: " + str(settings.get_Z_VALUE()))
        current_z_val.pack()
        current_parking_fee = tk.Label(tab3, text="parking_fee: " + str(settings.get_parking_fee()))
        current_parking_fee.pack()

        #Edit settings
        divider = tk.Label(tab3, text="----------------------------------------")
        divider.pack()
        edit_settings_label = tk.Label(tab3, text="Edit Settings: ")
        edit_settings_label.pack()
        #using label to show text
        x_val_label = tk.Label(tab3, text="x_val: ")
        x_val_label.pack()
        x_val_entry = tk.Entry(tab3)
        x_val_entry.pack()
        y_val_label = tk.Label(tab3, text="y_val: ")
        y_val_label.pack()
        y_val_entry = tk.Entry(tab3)
        y_val_entry.pack()
        z_val_label = tk.Label(tab3, text="z_val: ")
        z_val_label.pack()
        z_val_entry = tk.Entry(tab3)
        z_val_entry.pack()
        parking_fee_label = tk.Label(tab3, text="parking_fee: ")
        parking_fee_label.pack()
        parking_fee_entry = tk.Entry(tab3)
        parking_fee_entry.pack()
        password_label = tk.Label(tab3, text="password: ")
        password_label.pack()
        password_entry = tk.Entry(tab3)
        password_entry.pack()
        #using button to upload settings
        upload_button = tk.Button(tab3, text="Upload", command=lambda: self.upload_settings(x_val_entry,
                                                                                            y_val_entry,
                                                                                            z_val_entry,
                                                                                            password_entry,
                                                                                            parking_fee_entry))

        upload_button.pack()



        #tab4: History tab
        tab4 = ttk.Frame(tab_control)
        tab_control.add(tab4, text="History")
        tab_control.pack(expand=1, fill="both")
        #get history
        history = self.ms.get_history()
        #scrollbar x
        scrollbar_x = tk.Scrollbar(tab4, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        #scrollbar y
        scrollbar_y = tk.Scrollbar(tab4, orient=tk.VERTICAL)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        #using listbox to show history
        history_listbox = tk.Listbox(tab4, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        history_listbox.pack()
        #add history to listbox
        for h in history:
            history_listbox.insert(tk.END, h)
        #config scrollbar
        scrollbar_x.config(command=history_listbox.xview)
        scrollbar_y.config(command=history_listbox.yview)
        #config listbox size
        history_listbox.config(width=100, height=20)
        #add second listbox to show detail of history using select highlight
        history_detail_listbox = tk.Listbox(tab4, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        history_detail_listbox.pack()
        #config scrollbar
        scrollbar_x.config(command=history_detail_listbox.xview)
        scrollbar_y.config(command=history_detail_listbox.yview)
        #config listbox size
        history_detail_listbox.config(width=100, height=20)
        #using select highlight to show detail of history
        history_listbox.bind("<<ListboxSelect>>", lambda event: self.show_history_detail(history_listbox, history_detail_listbox, history))




        #tab5: about
        tab5 = ttk.Frame(tab_control)
        tab_control.add(tab5, text="About")
        tab_control.pack(expand=1, fill="both")

        #using label to show text
        about_label_devs = tk.Label(tab5, text="Developer: Le Tuan Huy(bi12-195) "
                                          "\nNguyen Minh Hoang(bi12-172)" 
                                          "\nLe Minh Hoang(bi12-167)" 
                                          "\nNguyen The Hoang(bi12-171)"
                                          "\nNguyen Vu Viet Hoang(bi12-173)")
        about_label_devs.pack()

        divider = tk.Label(tab5, text="----------------------------------------")
        divider.pack()

        about_label_contact = tk.Label(tab5, text="Contact:huylt.bi12-195@st.usth.edu.vn"
                                                  "\nhoangnm.bi12-172@st.usth.edu.vn"
                                                  "\nhoanglm.bi12-167@st.usth.edu.vn"
                                                  "\nhoangnt.bi12-171@st.usth.edu.vn"
                                                  "\nhoangnvv.bi12-173@st.usth.edu.vn")
        about_label_contact.pack()

        divider = tk.Label(tab5, text="----------------------------------------")
        divider.pack()

        about_label_description = tk.Label(tab5, text="This GUI is a emergency GUI for the parking building"
                                                        "\nIntended to be used in case of the main GUI is not working"
                                                      "\nor the main GUI resources is not available")
        about_label_description.pack()

        self.dashboard_window.mainloop()

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

    def show_history_detail(self, history_listbox, history_detail_listbox, history_lst):
        history_detail_listbox.delete(0, 'end')
        history_detail = history_lst[history_listbox.curselection()[0]]
        print(history_detail)
        #add dict(id, car_license_plate, car_driver_name, check_in_time, check_out_time, parking_fee, status, slot_code) to listbox
        history_detail_listbox.insert(tk.END, "ID: " + str(history_detail['id']))
        history_detail_listbox.insert(tk.END, "Car license plate: " + str(history_detail['car_license_plate']))
        history_detail_listbox.insert(tk.END, "Car driver name: " + str(history_detail['car_driver_name']))
        history_detail_listbox.insert(tk.END, "Check in time: " + str(history_detail['checkin_time']))
        history_detail_listbox.insert(tk.END, "Check out time: " + str(history_detail['checkout_time']))
        history_detail_listbox.insert(tk.END, "Parking fee: " + str(history_detail['checkout_fee']))
        history_detail_listbox.insert(tk.END, "Status: " + str(history_detail['status']))
        history_detail_listbox.insert(tk.END, "Slot code: " + str(history_detail['slot_code']))



    def refresh(self):
        self.dashboard_window.destroy()
        self.__init__()
        self.main_window()

class LoginWindow:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("400x300")
        self.login_window.resizable(True, True)
        self.lg = LoginVerification()

    def login_window_main(self):
        # create a label for password
        password_label = tk.Label(self.login_window, text="Password")
        password_label.pack()
        # create a entry for password
        password_entry = tk.Entry(self.login_window, show="*")
        password_entry.pack()
        # create a button for login
        login_button = tk.Button(self.login_window,
                                 text="Login",
                                 command=lambda: self.login_button(password_entry))
        login_button.pack()
        self.login_window.protocol("WM_DELETE_WINDOW", lambda: self.login_window.destroy())
        self.login_window.mainloop()

    def login_button(self, password_entry):
        password = password_entry.get()
        if self.lg.verify_password(password):
            password_entry.delete(0, tk.END)
            self.login_window.destroy()
            d = Dashboard()
            d.main_window()
        else:
            lbl = tk.Label(self.login_window, text="Wrong password")
            lbl.pack()
            password_entry.delete(0, tk.END)

if __name__ == "__main__":
    login = LoginWindow()
    login.login_window_main()