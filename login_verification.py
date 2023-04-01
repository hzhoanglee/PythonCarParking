from utils import IOdb
import bcrypt

class LoginVerification:
    def __init__(self):
        self.settings = IOdb.fetch_settings_db()
        self.password = self.settings[4]['conf_value']
        self.__hashed_password = self.hash_password_db()

    # ==================================================================================================================
    # hashing password from db
    def hash_password_db(self):
        return bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

    # ==================================================================================================================

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.__hashed_password):
            print("Password is correct")
            return True
        else:
            print("Password is incorrect")
            return False