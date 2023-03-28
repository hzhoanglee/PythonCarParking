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


def get_settings():
    dbconnection.execute("SELECT * FROM settings")
    settings = dbconnection.fetchall()
    return settings
