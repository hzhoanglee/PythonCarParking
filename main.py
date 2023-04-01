from login_verification import LoginVerification
from ManSys import ManagementSystem

if __name__ == "__main__":
    #settings = utils.connect.get_settings()
    #print(settings)

    lv = LoginVerification()
    result = lv.verify_password("admin")

    if result:
        print("Login success")
    else:
        print("Login failed")

    ms = ManagementSystem()
    ms.setup_parking_lot()
    #ms.checkin("Huy", "h1314")
    #ms.checkin("Jane", "456")
    #ms.checkin("Jack", "789")
    #ms.checkin("Hoang", "test1415", "A0-F2")
    #ms.checkout("B1-F1")
    #ms.get_slot_list()
    #ms.get_used_slot_count()
    #ms.get_available_slot_count()
    ms.get_unused_slots()
    print("=====================================")
    ms.get_used_slots()
    history = ms.get_history()
    for i in history:
        print(i)

    #gui = Dashboard()
    