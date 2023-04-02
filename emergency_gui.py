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
    def __init__(self):
        self.window = tk.Tk()
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
        tab_control = ttk.Notebook(self.window)
        for floor in self.building_floors:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=floor.get_floor_code())
            tab_control.pack(expand=1, fill="both")
            self.floor_window(tab, floor)
        self.window.mainloop()

    def floor_window(self, tab, floor):
        # create a button for each slot add to list
        slot_button_list = []
        for slot in floor.get_floor_slots():
            slot_button = tk.Button(tab, text=slot.get_slot_code(),
                                    command=lambda slot_code=slot.get_slot_code(): self.slot_window(slot_code))
            slot_button_list.append(slot_button)

        # use grid to place buttons in a table
        for i in range(len(slot_button_list)):
            row = i // len(self.x_list)
            col = i % len(self.x_list)
            slot_button_list[i].grid(row=row, column=col)

    def slot_window(self, slot_code):
        # create a window for each slot
        slot_window = tk.Toplevel(self.window)
        slot_window.title(slot_code)
        slot_window.geometry("400x300")
        slot_window.resizable(True, True)
        slot_window.grab_set()
        slot_window.focus_set()
        slot_window.transient(self.window)

        slot = ms.get_slot_by_code(slot_code)
        if slot.is_available():
            slot_button = tk.Button(slot_window, text="Check In", command=lambda: self.checkin_window(slot_code))
            slot_button.pack()
        else:
            slot_button = tk.Button(slot_window, text="Check Out", command=lambda: self.checkout_window(slot_code))
            slot_button.pack()

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
                                   command=lambda: ms.checkin(driver_name_entry.get(),
                                                              car_plate_entry.get(),
                                                              slot_code))
        checkin_button.pack()

    def checkout_window(self, slot_code):
        # create a window for checkout
        checkout_window = tk.Toplevel(self.window)
        checkout_window.title("Check Out")
        checkout_window.geometry("400x300")
        checkout_window.resizable(True, True)
        checkout_window.grab_set()
        checkout_window.focus_set()
        checkout_window.transient(self.window)

        # create a button for checkout
        checkout_button = tk.Button(checkout_window,
                                    text="Check Out",
                                    command=lambda: ms.checkout(slot_code))
        checkout_button.pack()


if __name__ == "__main__":
    gui = ParkingBuildingGUI()
    gui.main_window()
