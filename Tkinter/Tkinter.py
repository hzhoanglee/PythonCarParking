import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Create main tkinter window
r = tk.Tk ()
r.title = "Vịt Quay Pắcking"
r.geometry("600x300")

# Connect to DB
connect = mysql.connector.connect(host="sql.hz.edu.vn", user="python_parking", passwd="D6K2WTWAaSa7nFS2",
                                  database="python_parking", port="3306")

conn = connect.cursor()

conn.execute("SELECT * FROM check_ins")

tree = ttk.Treeview(r)

# Delete the 1st empty column
tree['show'] = 'headings'

# Define columns number
tree["columns"] = ("id", "plate", "owner", "checkin","checkout", "status", "slot")

# Individual column size
tree.column("id", width = 50, minwidth = 50, anchor=tk.CENTER)
tree.column("plate", width = 100, minwidth = 100, anchor=tk.CENTER)
tree.column("owner", width = 100, minwidth = 100, anchor=tk.CENTER)
tree.column("checkin", width = 150, minwidth = 150, anchor=tk.CENTER)
tree.column("checkout", width = 150, minwidth = 150, anchor=tk.CENTER)
tree.column("status", width = 50, minwidth = 50, anchor=tk.CENTER)
tree.column("slot", width = 100, minwidth = 100, anchor=tk.CENTER)

# Columns name
tree.heading("id", text = "ID", anchor = tk.CENTER)
tree.heading("plate", text = "License Plate", anchor = tk.CENTER)
tree.heading("owner", text = "Driver Name", anchor = tk.CENTER)
tree.heading("checkin", text = "Check-in Time", anchor = tk.CENTER)
tree.heading("checkout", text = "Check-out Time", anchor = tk.CENTER)
tree.heading("status", text = "Occupied", anchor = tk.CENTER)
tree.heading("slot", text = "Slot Code", anchor = tk.CENTER)


#
i = 0
for ro in conn:
    tree.insert("", i, text="", values = (ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
    i += 1


# Scroll bar
hsb = ttk.Scrollbar(r, orient = "horizontal")
hsb.configure(command = tree.xview)
tree.configure(xscrollcommand = hsb.set)
hsb.pack(fill = X, side = BOTTOM)

vsb = ttk.Scrollbar(r, orient = "vertical")
vsb.configure(command = tree.yview)
tree.configure(yscrollcommand = vsb.set)
vsb.pack(fill = Y, side = RIGHT)


tree.pack()
# Modify table
def add_row(tree):
    frame = Frame(r, width = 300, height = 150, background = "pink")
    frame.place(x = 100, y = 250)

    # ID
    lable1 = Label(frame, text = "ID", width = 8)
    entry1 = Entry(frame, textvariable = id, width = 25)
    lable1.place(x = 30, y = 20)
    entry1.place(x = 100, y = 20)

    #Plate
    #Owner
    #Checkin
    #Checkout
    #Status
    #Slot

# Button
insert_button = tk.Button(r, text = "Insert", command = lambda:add_row(tree))
insert_button.configure(font = ("calibri" ,10), bg = "white", fg = "green")
insert_button.place(x = 220, y = 250)

delete_button = tk.Button(r, text = "Delete", command = None)
delete_button.configure(font = ("calibri" ,10), bg = "white", fg = "red")
delete_button.place(x = 280, y = 250)

r.mainloop()
