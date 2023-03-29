class Slot:
    def __init__(self, slot_number):
        self.slot_number = slot_number
        self.car = None

    def is_available(self):
        return self.car is None

    def park(self, car):
        self.car = car

    def remove(self):
        self.car = None

    def get_car(self):
        return self.car

    def get_slot_number(self):
        return self.slot_number