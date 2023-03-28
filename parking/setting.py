class Settings:
    def __init__(self, X_VALUE=1, Y_VALUE=1, Z_VALUE=1, name="VitQuayParking", password=1234):
        self.__X_VALUE = X_VALUE
        self.__Y_VALUE = Y_VALUE
        self.__Z_VALUE = Z_VALUE
        self.__name = name
        self.__password = password

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
