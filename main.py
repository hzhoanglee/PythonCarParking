import utils.connect
from ManSys import ManagementSystem

if __name__ == "__main__":
    #settings = utils.connect.get_settings()
    #print(settings)

    ms = ManagementSystem()
    ms.setup_parking_lot()
    #ms.checkin("John", "123")
    #ms.checkin("Jane", "456")
    #ms.checkin("Jack", "789")

    ms.get_slot_list()

    ms.checkout("A3-F1")
