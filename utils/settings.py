import connect


def get_settings():
    connect.dbconnection.execute("SELECT * FROM settings")
    settings = connect.dbconnection.fetchall()
    return settings
