import utils.connect
from datetime import datetime

def fetch_settings_db():
    settings = utils.connect.get_settings()
    for setting in settings:
        print(setting)
    return settings

def fetch_check_ins_db():
    check_ins = utils.connect.get_check_ins()
    for check_in in check_ins:
        print(check_in)
    return check_ins

def update_settings_db(X_VALUE, Y_VALUE, Z_VALUE, name, password):
    utils.connect.update_settings(X_VALUE, Y_VALUE, Z_VALUE, name, password)

def update_check_ins_db(slot_id, driver_name, license_plate):
    utils.connect.update_check_ins(slot_id, driver_name, license_plate)

def check_out_db(slot_id):
    #now time
    now = datetime.now()
    result = utils.connect.check_out(slot_id)
    checkin_time = result['checkin_time']
    #calculate time difference(hours)
    datetime_diff = now - checkin_time
    #convert to hours(int)
    datetime_diff = int(datetime_diff.total_seconds() / 3600)
    return datetime_diff