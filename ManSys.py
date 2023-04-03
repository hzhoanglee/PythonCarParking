from utils.IOfuncs import IOfuncs
import bcrypt
class ManagementSystem:
    def __init__(self):
        #self.settings = fetch_settings()
        self.parking_slots = []
        self.io_car = IOfuncs(self.parking_slots)

    #==================================================================================================================
    def setup_parking_lot(self):
        self.io_car.setup_parking_lot()

    def checkin(self, driver_name, license_plate, slot_code):
        if driver_name is None or driver_name == '':
            print("Driver name is required")
            return -1
        if license_plate is None or license_plate == '':
            print("License plate is required")
            return -1
        self.io_car.checkin_car(driver_name, license_plate, slot_code)

    def checkout(self, slot_code):
        time_diff = self.io_car.checkout_car(slot_code)
        print("Time diff: ", time_diff)

        if time_diff < 24:
            parking_fee = int(self.io_car.get_parking_fee())
        else:
            parking_time = (time_diff / 24)
            if parking_time > int(parking_time):
                parking_fee = (int(parking_time)+1) * int(self.io_car.get_parking_fee())
            else:
                parking_fee = int(parking_time) * int(self.io_car.get_parking_fee())

        return parking_fee

    def edit_settings(self, X_VALUE, Y_VALUE, Z_VALUE, name, password):
        return self.io_car.edit_settings(X_VALUE, Y_VALUE, Z_VALUE, name, password)

    #==================================================================================================================
    def get_slot_list(self):
        return self.io_car.get_slot_list()

    def get_settings(self):
        settings = self.io_car.get_settings()
        return settings


    def get_unused_slots(self):
        for i in self.io_car.get_unused_slot():
            print(i.get_slot_code())
        return self.io_car.get_unused_slot()


    def get_used_slots(self):
        return self.io_car.get_used_slot()

    def get_max_slot_count(self):
        max_slot_count = self.io_car.get_max_slots_count()
        return max_slot_count

    def get_used_slot_count(self):
        used_slot_count = self.io_car.get_used_slot_count()
        return used_slot_count

    def get_available_slot_count(self):
        available_slot_count = self.io_car.get_available_slot_count()
        return available_slot_count


    def get_slot_by_code(self, slot_code):
        for slot in self.parking_slots:
            if slot.get_slot_code() == slot_code:
                return slot
    def get_history(self):
        return self.io_car.get_history()
    #def get_used_slot(self):
    #    self.get_used_slot()

