import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import *
import ManSys
from ManSys import ManagementSystem
from utils.connect import mydb


ms = ManagementSystem()
class table(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create main tkinter window
        self.r = tk.Tk()
        self.r.title = "Vịt Quay Pắcking"
        self.r.geometry("600x300")

        # Connect to DB
        self.dbconnection = mydb.cursor()
        self.dbconnection.execute("SELECT * FROM check_ins")

        self.tree = ttk.Treeview(self.r)

        # Delete the 1st empty column
        self.tree['show'] = 'headings'

        # Define columns number
        self.tree["columns"] = ("id", "plate", "owner", "checkin", "checkout", "status", "slot")

        # Individual column size
        self.tree.column("id", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("plate", width=100, minwidth=100, anchor=tk.CENTER)
        self.tree.column("owner", width=100, minwidth=100, anchor=tk.CENTER)
        self.tree.column("checkin", width=150, minwidth=150, anchor=tk.CENTER)
        self.tree.column("checkout", width=150, minwidth=150, anchor=tk.CENTER)
        self.tree.column("status", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("slot", width=100, minwidth=100, anchor=tk.CENTER)

        # Columns name
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.heading("plate", text="License Plate", anchor=tk.CENTER)
        self.tree.heading("owner", text="Driver Name", anchor=tk.CENTER)
        self.tree.heading("checkin", text="Check-in Time", anchor=tk.CENTER)
        self.tree.heading("checkout", text="Check-out Time", anchor=tk.CENTER)
        self.tree.heading("status", text="Occupied", anchor=tk.CENTER)
        self.tree.heading("slot", text="Slot Code", anchor=tk.CENTER)

        #
        self.i = 0
        for ro in self.dbconnection:
            self.tree.insert("", self.i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
            self.i += 1

        # Scroll bar
        self.hsb = ttk.Scrollbar(self.r, orient="horizontal")
        self.hsb.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.hsb.pack(fill=X, side=BOTTOM)

        self.vsb = ttk.Scrollbar(self.r, orient="vertical")
        self.vsb.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(fill=Y, side=RIGHT)

        self.tree.pack()
"""
        # Button
        self.insert_button = tk.Button(self.r, text="Insert", command=None)
        self.insert_button.configure(font=("calibri", 10), bg="white", fg="green")
        self.insert_button.place(x=220, y=250)

        self.delete_button = tk.Button(self.r, text="Delete", command= None)
        self.delete_button.configure(font=("calibri", 10), bg="white", fg="red")
        self.delete_button.place(x=280, y=250)


    def delete_row(self):
        selected_item = self.tree.selection()[0]
        #print(self.tree.item(selected_item)["value"])
        uid = tuple(self.tree.item(selected_item)['values'][:2])
        query = "DELETE FROM check_ins WHERE id=%S"
        selected_data = (uid,)
        self.dbconnection.execute(query, *(uid))
        self.connect.commit()
        self.tree.delete(selected_item)
        self.mb.showinfo("Success", "Car checked out")


"""

if __name__ == "__main__":
table = table()
table.mainloop()
