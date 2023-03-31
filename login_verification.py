from utils import IOdb
import bcrypt

class LoginVerification:
    def __init__(self):
        self.settings = IOdb.fetch_settings_db()
        self.name = self.settings[0]["name"]
        self.password = self.settings[0]["password"]
        self.__hashed_password = self.hash_password_db()

    # ==================================================================================================================
    # hashing password from db
    def hash_password_db(self):
        return bcrypt.hashpw(self.settings.get_password().encode('utf-8'), bcrypt.gensalt())

    # ==================================================================================================================

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.__hashed_password):
            print("Password is correct")
            return True
        else:
            print("Password is incorrect")
            return False