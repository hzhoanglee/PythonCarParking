import os
import mysql.connector
import time
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


def get_settings():
    dbconnection.execute("SELECT * FROM settings")
    settings = dbconnection.fetchall()
    return settings

def get_check_ins():
    dbconnection.execute("SELECT * FROM check_ins")
    check_ins = dbconnection.fetchall()
    return check_ins

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

def check_out(slot_id):
    #dbconnection.execute("SELECT checkin_time FROM check_ins WHERE slot_code = %s", (slot_id,))
    dbconnection.execute("SELECT TIMEDIFF(NOW(), checkin_time) AS timediff FROM check_ins WHERE slot_code = %s", (slot_id,))
    timediff = dbconnection.fetchone()
    dbconnection.execute("DELETE FROM check_ins WHERE slot_code = %s", (slot_id,))
    mydb.commit()
    return timediff



