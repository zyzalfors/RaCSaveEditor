import tkinter
from tkinter import ttk

class Combobox(ttk.Combobox):

    def __init__(self, root, name, val, vals):
        self.var = tkinter.StringVar()
        self.var.set(val)
        super().__init__(root, height = 1, width = 30, textvariable = self.var, state = "readonly")
        self.name = name
        self["values"] = tuple(vals)


    def getVal(self):
        return self.var.get()