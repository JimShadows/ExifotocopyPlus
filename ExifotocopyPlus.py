import os
import sys
from tkinter import *
from tkinter import StringVar, ttk
from tkinter import font
from tkinter.constants import E, N, S, W
from tkinter.ttk import Style

class ExifotocopyPlus():
    def __init__(self, root):

        root.title("ExifotocopyPlus")
        style=ttk.Style(root)
        style.theme_use("clam")
        style.configure(".",font=("Helverica", 12),foreground="snow")
        style.configure("TButton",background="gray20",activebackground="grey10", padding=6, relief="flat")    
        style.configure("TFrame",background="gray13")
        style.configure("TLabel",background="gray13")
        style.configure("TEntry",background="gray13",fieldbackground="grey16",bordercolor="grey10",lightcolor="grey10",relief="flat")

        style.configure("TCombobox",background="gray20",fieldbackground="grey16",selectbackground="dark orange",
        bordercolor="grey10",lightcolor="grey10",relief="RAISED", arrowcolor="dark orange",arrowsize=20,focusfill="red")
        root.option_add("*TCombobox*Listbox*Background", 'grey16')
        root.option_add("*TCombobox*Listbox.font", 'Helverica')
        root.option_add("*TCombobox*Listbox.foreground", 'snow')
        root.option_add("*TCombobox*Listbox.selectBackground", 'dark orange')
        root.option_add("TCombobox*Listbox.selectForeground", 'dark orange')
                
        style.configure("C.TFrame",background="dark orange")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #distacia de los objetos en el frame iz ar de abajo
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        leftframe=ttk.Frame(mainframe,borderwidth=5, width=25, style="C.TFrame")
        leftframe.grid(column=0,row=1,columnspan=1, padx=(10), pady=10)
        leftframe.columnconfigure(1,weight=1)
        leftframe.rowconfigure(1,weight=1)

         
        self.sourceDirectory =StringVar()
        self.targetDirectory=StringVar()
        self.filenameExtension=StringVar()
        self.formatStringLevel1Folder =StringVar()
        self.formatStringLevel2Folder =StringVar()
        self.formatStringLevel3Folder =StringVar()
        self.formatStringFilename =StringVar()
        self.numberFormatString= StringVar()
        self.logfile=StringVar()
        

        source_entry = ttk.Entry(mainframe, width=30, textvariable=self.sourceDirectory)
        source_entry.grid(column=2, row=1, sticky=(W))
        
        target_entry = ttk.Entry(mainframe, width=30, textvariable=self.targetDirectory)
        target_entry.grid(column=2, row=2, sticky=(W))

        filenameExtension_entry = ttk.Entry(mainframe, width=30, textvariable=self.filenameExtension)
        filenameExtension_entry.grid(column=2, row=3, sticky=(W))

        formatStringLevel1Folder_entry = ttk.Entry(mainframe, width=30, textvariable=self.formatStringLevel1Folder)
        formatStringLevel1Folder_entry.grid(column=2, row=4, sticky=(W))

        formatStringLevel2Folder_entry = ttk.Entry(mainframe, width=30, textvariable=self.formatStringLevel2Folder)
        formatStringLevel2Folder_entry.grid(column=2, row=5, sticky=(W))

        formatStringLevel3Folder_entry = ttk.Entry(mainframe, width=30, textvariable=self.formatStringLevel3Folder)
        formatStringLevel3Folder_entry.grid(column=2, row=6, sticky=(W))

        target_entry = ttk.Entry(mainframe, width=30, textvariable=self.targetDirectory)
        target_entry.grid(column=2, row=7, sticky=(W))


        self.imageResizevar = StringVar()
        imageResize = ttk.Combobox(mainframe, width=30, textvariable=self.imageResizevar)
        imageResize['values'] = ('1280x720',"1280x800","1600x900","1600x1200", '1980x1080',"1980x1200")
        imageResize.grid(column=2, row=7, sticky=(W))


        ttk.Button(mainframe, text="Execute", command=self.calculate).grid(column=2, row=10, sticky=E)

        ttk.Label(mainframe, text="Quellverzechnis").grid(column=1, row=1, sticky=(W,S))
        ttk.Label(mainframe, text="Zielverzeichnis").grid(column=1, row=2, sticky=(W,S))
        ttk.Label(mainframe, text="Dateinamenserweiterung").grid(column=1, row=3, sticky=(W,S))
        ttk.Label(mainframe, text="Dateinamenserweiterung").grid(column=1, row=4, sticky=(W,S))
        ttk.Label(mainframe, text="Tiefe der Verzeichnichsebene").grid(column=1, row=6, sticky=(W,S))


        sourceDirectoryPhoto = PhotoImage(file="images/Folder.png")
        ttk.Button(mainframe,image=sourceDirectoryPhoto, command=self.sourceDirectory).grid(column=3, row=1, sticky=E)

        

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        source_entry.focus()
        root.bind("<Return>", self.calculate)
        
    def calculate(self, *args):
            pass

    def sourceDirectory(self,*args):
        pass

root = Tk()
ExifotocopyPlus(root)
root.mainloop()