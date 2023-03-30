import parking
from parking.car import Car
from parking.slot import Slot
from parking.setting import Settings
from utils.IOdb import *

class IOfuncs:
    def __init__(self, slot_list):
        settings_fetch = fetch_settings_db()
        self.settings = Settings(settings_fetch[0]['conf_value'],
                                 settings_fetch[1]['conf_value'],
                                 settings_fetch[2]['conf_value'],
                                 settings_fetch[3]['conf_value'],
                                 settings_fetch[4]['conf_value'])
        self.slot_list = slot_list

    #==================================================================================================================
    #Input

    #setting up the parking lot
    def setup_parking_lot(self):
        x_list = []
        for i in range(int(self.settings.get_X_VALUE())):
            chars = [chr(i + 65)]
            x_list.append(chars)

        y_list = []
        for i in range(int(self.settings.get_Y_VALUE())):
            y_list.append(i)

        z_list = []
        for i in range(int(self.settings.get_Z_VALUE())):
            z_list.append(str("F" + str(i)))

        for i in x_list:
            for j in y_list:
                for k in z_list:
                    #format of slot id: A1-F0
                    gen_slot_code = f"{i[0]}{j}-{k}"
                    self.slot_list.append(Slot(gen_slot_code))
        online_slots = fetch_check_ins_db()

        for slot in self.slot_list:
            for online_slot in online_slots:
                if slot.get_slot_code() == online_slot['slot_code']:
                    slot.check_in(Car(online_slot['car_driver_name'], online_slot['car_license_plate']))


    #parking a car(checking in)
    def checkin_car(self, driver_name, license_plate):
        car = Car(driver_name, license_plate)
        for slot in self.slot_list:
            if slot.is_available():
                slot.check_in(car)
                update_check_ins_db(slot.get_slot_code(), driver_name, license_plate)
                break

    #remove a car(checking out)
    def checkout_car(self, slot_code):
        for slot in self.slot_list:
            if slot.get_slot_code() == slot_code:
                slot.check_out()
                datetime_diff = check_out_db(slot_code)
                return datetime_diff

    #edit settings
    def edit_settings(self, X_VALUE, Y_VALUE, Z_VALUE, name, password):
        self.settings.set_X_VALUE(X_VALUE)
        self.settings.set_Y_VALUE(Y_VALUE)
        self.settings.set_Z_VALUE(Z_VALUE)
        self.settings.set_name(name)
        self.settings.set_password(password)
        update_settings_db(X_VALUE, Y_VALUE, Z_VALUE, name, password)
        return self.settings
    #==================================================================================================================

    #output
    #get the list of slots
    def get_slot_list(self):
        return self.slot_list

    #get the list of settings
    def get_settings(self):
        return self.settings
