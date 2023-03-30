import utils.connect
from ManSys import ManagementSystem

if __name__ == "__main__":
    #settings = utils.connect.get_settings()
    #print(settings)

    ms = ManagementSystem()
    ms.setup_parking_lot()
    #ms.checkin("Huy", "h1314")
    #ms.checkin("Jane", "456")
    #ms.checkin("Jack", "789")
    #ms.checkin("Jack", "346")
    #ms.checkout("A0-F2")
    ms.get_slot_list()