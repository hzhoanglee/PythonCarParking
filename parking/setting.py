class Settings:
    def __init__(self, X_VALUE, Y_VALUE, Z_VALUE, name, password, parking_fee):
        self.__X_VALUE = X_VALUE
        self.__Y_VALUE = Y_VALUE
        self.__Z_VALUE = Z_VALUE
        self.__name = name
        self.__password = password
        self.__parking_fee = parking_fee

    def get_X_VALUE(self):
        return self.__X_VALUE

    def get_Y_VALUE(self):
        return self.__Y_VALUE

    def get_Z_VALUE(self):
        return self.__Z_VALUE

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def get_parking_fee(self):
        return self.__parking_fee

    #setters
    def set_X_VALUE(self, X_VALUE):
        if str(X_VALUE) == "" or X_VALUE is None:
            return -1
        elif str(X_VALUE).isdigit() is False:
            return -1
        self.__X_VALUE = X_VALUE

    def set_Y_VALUE(self, Y_VALUE):
        if str(Y_VALUE) == "" or Y_VALUE is None:
            return -1
        elif str(Y_VALUE).isdigit() is False:
            return -1
        self.__Y_VALUE = Y_VALUE

    def set_Z_VALUE(self, Z_VALUE):
        if str(Z_VALUE) == "" or Z_VALUE is None:
            return -1
        elif str(Z_VALUE).isdigit() is False:
            return -1
        self.__Z_VALUE = Z_VALUE

    def set_name(self, name):
        if name == "" or name is None:
            return -1
        self.__name = name

    def set_password(self, password):
        if password == "" or password is None:
            return -1
        self.__password = password

    def set_parking_fee(self, parking_fee):
        if str(parking_fee) == "" or parking_fee is None:
            return -1
        elif str(parking_fee).isdigit() is False:
            return -1
        self.__parking_fee = parking_fee
