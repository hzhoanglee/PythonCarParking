import utils.connect

#=======================================================================================================================
def fetch_settings_db():
    utils.connect.dbconnection.execute("SELECT * FROM settings")
    settings = utils.connect.dbconnection.fetchall()
    return settings

def fetch_check_ins_db():
    utils.connect.dbconnection.execute("SELECT * FROM check_ins")
    check_ins = utils.connect.dbconnection.fetchall()
    for check_in in check_ins:
        if check_in['status'] == 0:
            check_ins.remove(check_in)
    for check_in in check_ins:
        print(check_in)
    return check_ins

def fetch_history_db():
    utils.connect.dbconnection.execute("SELECT * FROM check_ins")
    check_ins = utils.connect.dbconnection.fetchall()
    #for check_in in check_ins:
    #    if check_in['status'] == 1:
    #        check_ins.remove(check_in)
    for check_in in check_ins:
        print(check_in)
    return check_ins

def fetch_used_slots_db():
    utils.connect.dbconnection.execute("SELECT * FROM check_ins WHERE status = 1")
    used_slots = utils.connect.dbconnection.fetchall()
    for used_slot in used_slots:
        print(used_slot)
    return used_slots


def fetch_used_slot_count_db():
    utils.connect.dbconnection.execute("SELECT COUNT(slot_code) FROM check_ins WHERE status = 1 ")
    used_slots_count = utils.connect.dbconnection.fetchall()
    used_slots_count = used_slots_count[0]["COUNT(slot_code)"]
    return used_slots_count

def fetch_unused_slot_count_db(max_slots_count):
    unused_slots_count = max_slots_count - fetch_used_slot_count_db()
    return unused_slots_count

def fetch_info_from_plate(license_plate):
    utils.connect.dbconnection.execute("SELECT car_driver_name, checkin_time, slot_code "
                                 "FROM check_ins "
                                 "WHERE car_license_plate = %s", (license_plate,))
    car_info = utils.connect.dbconnection.fetchall()
    return car_info

def fetch_info_from_slot(slot_code):
    utils.connect.dbconnection.execute(
        "SELECT TIMEDIFF(NOW(), checkin_time) AS timediff, car_driver_name, checkin_time, car_license_plate "
        "FROM check_ins "
        "WHERE slot_code = %s", (slot_code,))
    car_info = utils.connect.dbconnection.fetchall()
    return car_info

#=======================================================================================================================
def update_settings_db(X_VALUE, Y_VALUE, Z_VALUE, name, password):
    utils.connect.update_settings(X_VALUE, Y_VALUE, Z_VALUE, name, password)

def update_settings_name(name):
    utils.connect.dbconnection.execute("UPDATE settings SET name = %s", (name,))
    utils.connect.mydb.commit()

def update_settings_password(password):
    utils.connect.dbconnection.execute("UPDATE settings SET password = %s", (password,))
    utils.connect.mydb.commit()

def update_settings_X_VALUE(X_VALUE):
    utils.connect.dbconnection.execute("UPDATE settings SET X_VALUE = %s", (X_VALUE,))
    utils.connect.mydb.commit()

def update_settings_Y_VALUE(Y_VALUE):
    utils.connect.dbconnection.execute("UPDATE settings SET Y_VALUE = %s", (Y_VALUE,))
    utils.connect.mydb.commit()

def update_settings_Z_VALUE(Z_VALUE):
    utils.connect.dbconnection.execute("UPDATE settings SET Z_VALUE = %s", (Z_VALUE,))
    utils.connect.mydb.commit()

def update_check_ins_db(slot_id, driver_name, license_plate):
    utils.connect.dbconnection.execute("INSERT INTO check_ins (slot_code, car_driver_name, car_license_plate) "
                         "VALUES (%s, %s, %s)",
                         (slot_id, driver_name, license_plate))
    utils.connect.mydb.commit()

def check_out_db(slot_code):
    #get the time diff from the db sql
    utils.connect.dbconnection.execute("SELECT TIMEDIFF(NOW(), checkin_time) AS timediff FROM check_ins WHERE slot_code = %s",
                         (slot_code,))
    timediff = utils.connect.dbconnection.fetchall()
    #update the checkout time and status
    utils.connect.dbconnection.execute("UPDATE check_ins SET checkout_time = NOW(), status = 0 WHERE slot_code = %s AND status = 1", (slot_code,))
    utils.connect.mydb.commit()
    #convert the time diff to hours(int)
    datetime_diff = timediff[0]["timediff"]
    hours = int(datetime_diff.total_seconds() / 3600)
    return hours

#=======================================================================================================================