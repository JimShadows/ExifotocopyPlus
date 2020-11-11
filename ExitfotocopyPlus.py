import os
import sys
from tkinter import *
from tkinter import StringVar, ttk
from tkinter import font
from tkinter.constants import E, N, S, W


class ExitfotocopyPlus():
    def __init__(self, root):

        root.title("ExitfotocopyPlus")
        styleFrame=ttk.Style(root)
        styleFrame.theme_use("clam")
        styleFrame.configure('clam', background='darkgrey', borderwidth=5, relief='raised')
        #styleFrame.theme
        styleFrame.configure("TButton", padding=6, relief="flat",background="#ccc")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #distacia de los objetos en el frame iz ar de abajo
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        
       

        self.feet = StringVar()
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meters = StringVar()

        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="Quellverzechnis").grid(column=1, row=1, sticky=E)
        ttk.Label(mainframe, text="Zielverzeichnis").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="Zielverzeichnis").grid(column=1, row=3, sticky=E)
        ttk.Label(mainframe, text="Zielverzeichnis").grid(column=1, row=4, sticky=E)
        ttk.Label(mainframe, text="Zielverzeichnis").grid(column=1, row=6, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
        

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)
        
    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

root = Tk()
ExitfotocopyPlus(root)
root.mainloop()