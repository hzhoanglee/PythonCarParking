class Car:
    def __init__(self, driver_name, license_plate):
        self.driver_name = driver_name
        self.license_plate = license_plate

    def get_driver_name(self):
        return self.driver_name

    def get_license_plate(self):
        return self.license_plate

    def set_driver_name(self, driver_name):
        self.driver_name = driver_name

    def set_license_plate(self, license_plate):
        self.license_plate = license_plate
        