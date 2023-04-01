import customtkinter as ttk
from PIL import Image
from time import strftime
from ManSys import ManagementSystem

# Setting the theme for the main window
ttk.set_appearance_mode('light')
mainColor = "#8685ef"
sideColor = "#faf8ff"
mainScreenColor = '#f2ecff'
frameColor = '#e9e1ff'
grayColor = '#737373'

# Setting the main window
root = ttk.CTk()
root.geometry('800x600')
root.resizable(False, False)
root.title("Vịt Quay Parking System")
root.config(background='#f2ecff')


# ================================================
# ===================FUNCTIONS====================
# ================================================

# Creating date/time
def my_time():
    time_string = strftime('%H:%M:%S %p \n %A \n %x')
    l1.configure(text=time_string)
    l1.after(1000, my_time)  # time delay of 1000 milliseconds


# New window when a sidebar button is clicked
def open_check_in():
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Car Check In Window")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 300, y + 150))
    new.geometry('500x450')

    # form
    ttk.CTkLabel(master=new,
                 text="Car Check In",
                 text_color=grayColor,
                 font=('', 20, 'bold'),
                 fg_color=mainScreenColor, ).place(x=100, y=90)

    ttk.CTkEntry(master=new,
                 width=300,
                 height=40,
                 placeholder_text='Driver Name',
                 bg_color=mainScreenColor).place(x=100, y=140)

    ttk.CTkEntry(master=new,
                 width=300,
                 height=40,
                 placeholder_text='License plate',
                 bg_color=frameColor
                 ).place(x=100, y=195)

    ttk.CTkEntry(master=new,
                 width=300,
                 height=40,
                 placeholder_text='Slot code',
                 bg_color=mainScreenColor
                 ).place(x=100, y=250)

    # Submit button
    def save_data():
        # Have to implement a getter
        print('A car have been added')

    ttk.CTkButton(master=new,
                  text="Add car",
                  fg_color=mainColor,
                  font=("", 15, 'bold'),
                  text_color='white',
                  cursor="hand2",
                  hover_color='#ccccff',
                  command=save_data()).place(x=100, y=320)

    # Keep the toplevel window in front of the root window
    new.wm_transient(root)

    new.mainloop()


def open_manage():
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("Manage Car Window")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 250, y + 100))
    new.geometry('600x520')


    new.wm_transient(root)
    new.mainloop()


def open_history():
    # Creating the screen
    new = ttk.CTkToplevel(root)
    new.resizable(False, False)
    new.title("History")
    new.config(background=mainScreenColor)
    x = root.winfo_x()
    y = root.winfo_y()
    new.geometry("+%d+%d" % (x + 250, y + 100))
    new.geometry('600x520')

    # Displaying history


    new.wm_transient(root)
    new.mainloop()


# ================================================
# ===================END OF FUNCTIONS=============
# ================================================

# ====================================
# =============HEADER=================
# ====================================

# Creating the header
header = ttk.CTkFrame(root,
                      width=1070,
                      height=60,
                      fg_color="#8685ef")
header.place(x=201, y=0)

# Log out button
logout_text = ttk.CTkButton(header,
                            text="Logout",
                            font=("", 13, "bold"),
                            fg_color='white',
                            cursor='hand2',
                            text_color=mainColor,
                            hover_color='#ccccff')
logout_text.place(x=450, y=15)

# ====================================
# =============END OF HEADER==========
# ====================================

# ===============================================
# =====================SIDEBAR===================
# ===============================================

# Sidebar
sideBar = ttk.CTkFrame(master=root, width=200,
                       height=1300,
                       fg_color="#faf8ff")
sideBar.place(x=0, y=0)

# Logo
logoImage = ttk.CTkImage(light_image=Image.open("images/icon.png"),
                         size=(100, 100))
logo = ttk.CTkLabel(sideBar,
                    text='',
                    image=logoImage)
logo.place(x=50, y=80)

# Name of the person
name = ttk.CTkLabel(master=sideBar,
                    text="ADMIN",
                    font=("", 15, "bold"),
                    text_color="#737373")
name.place(x=75, y=180)

# ===============================================
# =====================BUTTONS===================
# ===============================================

# Home
homeImage = ttk.CTkImage(light_image=Image.open('images/home.png'),
                         size=(25, 25))
homeButton = ttk.CTkButton(master=sideBar,
                           image=homeImage,
                           text="Home",
                           width=200,
                           height=50,
                           compound='left',
                           fg_color='transparent',
                           text_color=mainColor,
                           font=('', 15, 'bold'),
                           cursor="hand2",
                           hover_color='#ccccff').place(x=0, y=250)

# Car check in
carImage = ttk.CTkImage(light_image=Image.open('images/car.png'),
                        size=(25, 25))

carButton = ttk.CTkButton(master=sideBar,
                          image=carImage,
                          text="Car check-in",
                          width=200,
                          height=50,
                          compound='left',
                          fg_color='transparent',
                          text_color=mainColor,
                          font=('', 15, 'bold'),
                          cursor="hand2",
                          anchor='center',
                          hover_color='#ccccff',
                          command=lambda: open_check_in(),
                          ).place(x=0, y=300)

# Manage vehicle

manageImage = ttk.CTkImage(light_image=Image.open('images/manage.png'),
                           size=(20, 20))
manageButton = ttk.CTkButton(master=sideBar,
                             image=manageImage,
                             text="Manage vehicle",
                             width=200,
                             height=50,
                             compound='left',
                             fg_color='transparent',
                             text_color=mainColor,
                             font=('', 15, 'bold'),
                             cursor="hand2",
                             anchor='center',
                             hover_color='#ccccff',
                             command=lambda: open_manage()
                             ).place(x=0, y=350)

# History
historyImage = ttk.CTkImage(light_image=Image.open('images/history.png'),
                            size=(25, 25))
historyButton = ttk.CTkButton(master=sideBar,
                              image=historyImage,
                              text="History",
                              width=200,
                              height=50,
                              compound='left',
                              fg_color='transparent',
                              text_color=mainColor,
                              font=('', 15, 'bold'),
                              cursor="hand2",
                              anchor='center',
                              hover_color='#ccccff').place(x=0, y=400)

# ===============================================
# =====================END OF BUTTONS============
# ===============================================

# ===============================================
# =====================TIME======================
# ===============================================


l1 = ttk.CTkLabel(master=sideBar, font=('', 15, 'bold'), text_color=grayColor)
l1.place(x=50, y=480)

# ===============================================
# =====================END OF TIME===============
# ===============================================

# ======================================================
# =====================END OF SIDEBAR===================
# ======================================================


# ======================================================
# =====================MAIN SCREEN======================
# ======================================================





my_time()
root.mainloop()
