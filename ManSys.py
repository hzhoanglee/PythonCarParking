from utils.IOfuncs import IOfuncs

class ManagementSystem:
    def __init__(self):
        #self.settings = fetch_settings()
        self.parking_slots = []
        self.io_car = IOfuncs(self.parking_slots)

    def setup_parking_lot(self):
        self.io_car.setup_parking_lot()

    def checkin(self, driver_name, license_plate):
        self.io_car.checkin_car(driver_name, license_plate)

    def checkout(self, slot_id):
        time_diff = self.io_car.checkout_car(slot_id)
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

    def get_slot_list(self):
        for i in self.io_car.get_slot_list():
            if not i.is_available():
                print(i.get_slot_id(), i.get_car().get_driver_name(), i.get_car().get_license_plate())

    def get_settings(self):
        for i in self.io_car.get_settings():
            print(i)

