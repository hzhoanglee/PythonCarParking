import connect


def get_settings():
    connect.dbconnection.execute("SELECT * FROM settings")
    settings = connect.dbconnection.fetchall()
    return settings


def update_settings_name(name):
    connect.dbconnection.execute("UPDATE settings SET name = %s", (name,))
    connect.mydb.commit()


def update_settings_password(password):
    connect.dbconnection.execute("UPDATE settings SET password = %s", (password,))
    connect.mydb.commit()


def update_settings_X_VALUE(X_VALUE):
    connect.dbconnection.execute("UPDATE settings SET X_VALUE = %s", (X_VALUE,))
    connect.mydb.commit()


def update_settings_Y_VALUE(Y_VALUE):
    connect.dbconnection.execute("UPDATE settings SET Y_VALUE = %s", (Y_VALUE,))
    connect.mydb.commit()


def update_settings_Z_VALUE(Z_VALUE):
    connect.dbconnection.execute("UPDATE settings SET Z_VALUE = %s", (Z_VALUE,))
    connect.mydb.commit()
