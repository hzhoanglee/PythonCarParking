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
        self.io_car.checkin_car(driver_name, license_plate, slot_code)

    def checkout(self, slot_code):
        time_diff = self.io_car.checkout_car(slot_code)
        print("Time diff: ", time_diff)

        if time_diff < 7:
            print("You have to pay 2000 vnd")
            return 2000
        elif time_diff < 18:
            print("You have to pay 3000 vnd")
            return 3000
        else:
            print("You have to pay 5000 vnd")
            return 5000

    def edit_settings(self, X_VALUE, Y_VALUE, Z_VALUE, name, password):
        return self.io_car.edit_settings(X_VALUE, Y_VALUE, Z_VALUE, name, password)

    #==================================================================================================================
    def get_slot_list(self):
        for i in self.io_car.get_slot_list():
            if not i.is_available():
                print(i.get_slot_code(), i.get_car().get_driver_name(), i.get_car().get_license_plate())

    def get_settings(self):
        settings = self.io_car.get_settings()
        for i in settings:
            print(i)
        return settings


    def get_unused_slots(self):
        for i in self.io_car.get_unused_slot():
            print(i.get_slot_code())
        return self.io_car.get_unused_slot()


    def get_used_slots(self):
        return self.io_car.get_used_slot()

    def get_used_slot_count(self):
        used_slot_count = self.io_car.get_used_slot_count()
        return used_slot_count

    def get_available_slot_count(self):
        available_slot_count = self.io_car.get_available_slot_count()
        return available_slot_count

    def get_history(self):
        return self.io_car.get_history()
    #def get_used_slot(self):
    #    self.get_used_slot()

