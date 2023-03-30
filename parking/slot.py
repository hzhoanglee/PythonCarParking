class Slot:
    def __init__(self, slot_code):
        self.slot_code = slot_code
        self.car = None

    def is_available(self):
        return self.car is None

    def check_in(self, car):
        self.car = car

    def check_out(self):
        self.car = None

    def get_car(self):
        return self.car

    def get_slot_code(self):
        return self.slot_code