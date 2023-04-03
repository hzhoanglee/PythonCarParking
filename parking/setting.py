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
        self.__X_VALUE = X_VALUE

    def set_Y_VALUE(self, Y_VALUE):
        self.__Y_VALUE = Y_VALUE

    def set_Z_VALUE(self, Z_VALUE):
        self.__Z_VALUE = Z_VALUE

    def set_name(self, name):
        self.__name = name

    def set_password(self, password):
        self.__password = password

    def set_parking_fee(self, parking_fee):
        self.__parking_fee = parking_fee
