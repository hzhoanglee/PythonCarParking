from utils.IOfuncs import IOfuncs
import datetime
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

        self.io_car.update_history_fee(slot_code, parking_fee)
        return parking_fee

    def edit_settings(self, X_VALUE, Y_VALUE, Z_VALUE, password, parking_fee):
        return self.io_car.edit_settings(X_VALUE, Y_VALUE, Z_VALUE, password, parking_fee)

    def change_password(self, new_pass):
        self.io_car.change_password(new_pass)
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

    def get_daily_report(self):
        daily_report = []
        f = '%Y-%m-%d'
        for i in self.io_car.get_history():
            if i is None or i['checkout_time'] is None:
                continue
            else:
                checkout_time = i['checkout_time'].strftime(f)
                if checkout_time == datetime.datetime.now().strftime(f):
                    daily_report.append(i)
        print(daily_report)
        return daily_report

    def get_monthly_report(self):
        monthly_report = []
        f = '%Y-%m'
        for i in self.io_car.get_history():
            if i is None or i['checkout_time'] is None:
                continue
            else:
                checkout_time = i['checkout_time'].strftime(f)
                if checkout_time == datetime.datetime.now().strftime(f):
                    monthly_report.append(i)
        print(monthly_report)
        return monthly_report

    def get_yearly_report(self):
        yearly_report = []
        f = '%Y'
        for i in self.io_car.get_history():
            if i is None or i['checkout_time'] is None:
                continue
            else:
                checkout_time = i['checkout_time'].strftime(f)
                if checkout_time == datetime.datetime.now().strftime(f):
                    yearly_report.append(i)
        print(yearly_report)
        return yearly_report

    def calculate_total_income(self, report):
        total_income = 0
        for i in report:
            if i is None or i['checkout_fee'] is None:
                continue
            else:
                total_income += int(i['checkout_fee'])
        print(total_income)
        return total_income

    def get_history_details(self, index, history_lst):
        return self.io_car.get_history_details(index, history_lst)

