import customtkinter as ttk
from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from datetime import *
import time
import pymysql

# Setting the theme of the window
ttk.set_appearance_mode('light')
mainColor = "#8685ef"
sideColor = "#faf8ff"

# Securing a connection with mysql
connect = pymysql.connect(host="localhost", user='root', passwd="", database="")
cursor = connect.cursor()


class Dashboard:
    def __init__(self, root):
        self.mainScreen = None
        self.root = root
        self.root.geometry('1000x550')
        self.root.resizable(False, False)
        self.root.title("Vịt Quay Parking System")
        self.root.config(background='#f2ecff')

        # ====================================
        # =============HEADER=================
        # ====================================

        # Creating the header
        self.header = ttk.CTkFrame(self.root,
                                   width=1070,
                                   height=60,
                                   fg_color="#8685ef")
        self.header.place(x=201, y=0)

        # Log out button
        self.logout_text = ttk.CTkButton(self.header,
                                         text="Logout",
                                         font=("", 13, "bold"),
                                         fg_color='white',
                                         cursor='hand2',
                                         text_color=mainColor,
                                         hover_color='#ccccff')
        self.logout_text.place(x=640, y=15)

        # ====================================
        # =============END OF HEADER==========
        # ====================================

        # ====================================
        # =============SIDEBAR=================
        # ====================================

        # Creating the sidebar
        self.sidebar = ttk.CTkFrame(self.root,
                                    width=200,
                                    height=1300,
                                    fg_color="#faf8ff")
        self.sidebar.place(x=0, y=0)

        # Logo
        self.logoImage = ttk.CTkImage(light_image=Image.open('images/icon.png'),
                                      size=(100, 100))
        self.logo = ttk.CTkLabel(self.sidebar,
                                 text='',
                                 image=self.logoImage)
        self.logo.place(x=50, y=80)

        # Name of the person
        self.name = ttk.CTkLabel(master=self.sidebar,
                                 text="ADMIN",
                                 font=("", 15, "bold"),
                                 text_color="#737373")
        self.name.place(x=75, y=180)

        # Home
        self.homeImage = ttk.CTkImage(light_image=Image.open('images/home.png'),
                                      size=(25, 25))
        self.homeButton = ttk.CTkButton(master=self.sidebar,
                                        image=self.homeImage,
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
        self.carImage = ttk.CTkImage(light_image=Image.open('images/car.png'),
                                     size=(25, 25))
        self.carButton = ttk.CTkButton(master=self.sidebar,
                                       image=self.carImage,
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
                                       ).place(x=0, y=300)
        self.toplevel_window = None

        # Manage vehicle

        self.manageImage = ttk.CTkImage(light_image=Image.open('images/manage.png'),
                                        size=(20, 20))
        self.manageButton = ttk.CTkButton(master=self.sidebar,
                                          image=self.manageImage,
                                          text="Manage vehicle",
                                          width=200,
                                          height=50,
                                          compound='left',
                                          fg_color='transparent',
                                          text_color=mainColor,
                                          font=('', 15, 'bold'),
                                          cursor="hand2",
                                          anchor='center',
                                          hover_color='#ccccff').place(x=0, y=350)

        # History
        self.historyImage = ttk.CTkImage(light_image=Image.open('images/history.png'),
                                         size=(25, 25))
        self.historyButton = ttk.CTkButton(master=self.sidebar,
                                           image=self.historyImage,
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

        # date and Time
        self.date_time = ttk.CTkLabel(self.root)
        self.date_time.place(x=60, y=480)
        self.show_time()

        # Frames
        self.frame1 = ttk.CTkFrame(master=self.root, width=790, height=470).place(x=205, y=70)

    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%Y/%m/%d')
        set_text = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=set_text, font=("", 15, "bold"), bg_color='#faf8ff', text_color='#737373')
        self.date_time.after(100, self.show_time)

        # ====================================
        # =============END OF SIDEBAR=========
        # ====================================

        # ====================================
        # =============MAIN SCREEN============
        # ====================================


def window():
    root = ttk.CTk()
    Dashboard(root)
    root.mainloop()


if __name__ == '__main__':
    window()
