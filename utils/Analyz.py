import connect
import IOfuncs


def get_used_slot():
    connect.dbconnection.execute("SELECT COUNT(slot_code) FROM check_ins")
    slot_count = connect.dbconnection.fetchall()
    return slot_count


def get_unused_slot():
    used_slot = get_used_slot()
    slot_count = len(IOfuncs.get_slot_list()) - used_slot
    return slot_count

# Slots used within floors


def check_floor(floor):
    connect.dbconnection.execute("SELECT COUNT(car_driver_name) "
                                 "FROM check_ins "
                                 "WHERE RIGHT(slot_code, 1) = %s", (floor,))
    slot_count = connect.dbconnection.fetchall()
    return slot_count

# Check infor of a car with exact conditions


def check_plate(license_plate):
    connect.dbconnection.execute("SELECT car_driver_name, checkin_time, slot_code "
                                 "FROM check_ins "
                                 "WHERE car_license_plate = %s", (license_plate,))
    car_info = connect.dbconnection.fetchall()
    return car_info


def check_slot(slot_id):
    connect.dbconnection.execute("SELECT TIMEDIFF(NOW(), checkin_time) AS timediff, car_driver_name, checkin_time, car_license_plate "
                                 "FROM check_ins "
                                 "WHERE slot_code = %s", (slot_id,))
    car_info = connect.dbconnection.fetchall()
    return car_info
