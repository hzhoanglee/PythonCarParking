import tkinter as tk
from tkinter import ttk
from ManSys import ManagementSystem

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


class ParkingBuildingGUI:
    def __init__(self, tk_window):
        self.window = tk_window
        self.window.title("Parking Building")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

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
            if ms.get_slot_by_code(slot_code).is_available():
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

        slot = ms.get_slot_by_code(slot_code)
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
        ms.checkin(driver_name, car_plate, slot_code)
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
        fee = ms.checkout(slot_code)
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
        self.dashboard_window = tk.Tk()
        self.ParkingBuildingGUI = ParkingBuildingGUI(self.dashboard_window)
        self.dashboard_window.title("Dashboard")
        # dashboard window must bigger than ParkingBuildingGUI
        self.dashboard_window.geometry("1000x800")
        self.dashboard_window.resizable(True, True)

    def main_window(self):
        # using notebook to create tabs, each tab is a window to show different content
        #1. is the parking building map (ParkingBuildingGUI)
        #2. is the about and help content, contact us (N/a)

        tab_control = ttk.Notebook(self.dashboard_window)
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


        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text="General Info")
        tab_control.pack(expand=1, fill="both")
        # get max slot number
        max_slot_number = ms.get_max_slot_count()
        # get used slot number
        used_slot_number = ms.io_car.get_used_slot_count()
        # get free slot number
        free_slot_number = ms.io_car.get_available_slot_count()

        # using label to show text
        general_info_label = tk.Label(tab2, text="Max Slot Number: " + str(max_slot_number)
                                        + "\nUsed Slot Number: " + str(used_slot_number)
                                        + "\nFree Slot Number: " + str(free_slot_number))
        general_info_label.pack()


        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text="About")
        tab_control.pack(expand=1, fill="both")
        #add some line of text to tab3
        # Developer: Le Tuan Huy(LTH3ar)
        # Contact: huylt.bi12-195@st.usth.edu.vn
        # This GUI is a emergency GUI for the parking building
        # It is not a final version, it is just a prototype

        #using label to show text
        about_label = tk.Label(tab3, text="Developer: Le Tuan Huy(LTH3ar)"
                                          "\nContact: huylt.bi12-195@st.usth.edu.vn"
                                            "\nThis GUI is an emergency GUI for the parking system"
                                            "\nIt is not a final version, it is just a prototype")
        about_label.pack()


        self.dashboard_window.mainloop()

    def refresh(self):
        self.dashboard_window.destroy()
        self.__init__()
        self.main_window()
if __name__ == "__main__":
    d = Dashboard()
    d.main_window()
