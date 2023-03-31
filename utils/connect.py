import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
    port=os.getenv("DB_PORT")
)

dbconnection = mydb.cursor(dictionary=True)

#getter(output)
#=======================================================================================================================
def get_settings():
    dbconnection.execute("SELECT * FROM settings")
    settings = dbconnection.fetchall()
    return settings

def get_check_ins():
    dbconnection.execute("SELECT * FROM check_ins")
    check_ins = dbconnection.fetchall()
    return check_ins

def get_used_slots():
    dbconnection.execute("SELECT * FROM check_ins WHERE status = 1")
    used_slots = dbconnection.fetchall()
    return used_slots

def get_used_slot_count():
    dbconnection.execute("SELECT COUNT(slot_code) FROM check_ins")
    slot_count = dbconnection.fetchall()
    slot_count = slot_count[0]["COUNT(slot_code)"]
    return slot_count

def check_floor(floor):
    dbconnection.execute("SELECT COUNT(car_driver_name) "
                                 "FROM check_ins "
                                 "WHERE RIGHT(slot_code, 1) = %s", (floor,))
    slot_count = dbconnection.fetchall()
    return slot_count

def check_plate(license_plate):
    dbconnection.execute("SELECT car_driver_name, checkin_time, slot_code "
                                 "FROM check_ins "
                                 "WHERE car_license_plate = %s", (license_plate,))
    car_info = dbconnection.fetchall()
    return car_info

def check_slot(slot_id):
    dbconnection.execute("SELECT TIMEDIFF(NOW(), checkin_time) AS timediff, car_driver_name, checkin_time, car_license_plate "
                                 "FROM check_ins "
                                 "WHERE slot_code = %s", (slot_id,))
    car_info = dbconnection.fetchall()
    return car_info


#setter(input)
#=======================================================================================================================
def update_settings(X_VALUE, Y_VALUE, Z_VALUE, name, password):
    dbconnection.execute("UPDATE settings SET conf_value = %s WHERE conf_name = 'X_VALUE'", (X_VALUE,))
    dbconnection.execute("UPDATE settings SET conf_value = %s WHERE conf_name = 'Y_VALUE'", (Y_VALUE,))
    dbconnection.execute("UPDATE settings SET conf_value = %s WHERE conf_name = 'Z_VALUE'", (Z_VALUE,))
    dbconnection.execute("UPDATE settings SET conf_value = %s WHERE conf_name = 'name'", (name,))
    dbconnection.execute("UPDATE settings SET conf_value = %s WHERE conf_name = 'password'", (password,))
    mydb.commit()

def update_check_ins(slot_id, driver_name, license_plate):
    dbconnection.execute("INSERT INTO check_ins (slot_code, car_driver_name, car_license_plate) "
                         "VALUES (%s, %s, %s)",
                         (slot_id, driver_name, license_plate))
    mydb.commit()

def check_out(slot_code):
    #dbconnection.execute("SELECT checkin_time FROM check_ins WHERE slot_code = %s", (slot_id,))
    dbconnection.execute("SELECT TIMEDIFF(NOW(), checkin_time) AS timediff FROM check_ins WHERE slot_code = %s", (slot_code,))
    timediff = dbconnection.fetchone()
    #dbconnection.execute("DELETE FROM check_ins WHERE slot_code = %s", (slot_id,))
    dbconnection.execute("UPDATE check_ins SET checkout_time = NOW(), status = 0 WHERE slot_code = %s", (slot_code,))

    mydb.commit()
    return timediff
#=======================================================================================================================



