import tkinter
from tkinter import ttk

class Checkbox(tkinter.Checkbutton):

    def __init__(self, parent, text):
        super().__init__(master = parent, text = text, onvalue = 1, offvalue = 0)


    def setVal(self, val):
        self.select() if val else self.deselect()


    def getVal(self):
        return bool(self.getvar(self.cget("variable")))


class Combobox(ttk.Combobox):

    def __init__(self, parent, vals, width):
        super().__init__(master = parent, width = width, values = vals, state = "readonly")


    def setVal(self, val):
        self.set(val)


    def getVal(self):
        return self.get()


class Tab(ttk.Frame):

    def __init__(self, parent, width, height):
        super().__init__(master = parent)

        self.canvas = tkinter.Canvas(master = self, highlightthickness = 0, bd = 0)
        self.content = ttk.Frame(master = self.canvas)

        vbar = ttk.Scrollbar(master = self, orient = "vertical", command = self.canvas.yview)
        hbar = ttk.Scrollbar(master = self, orient = "horizontal", command = self.canvas.xview)

        self.canvas.configure(yscrollcommand = vbar.set, xscrollcommand = hbar.set)
        self.canvas.create_window(0, 0, window = self.content, anchor = "nw")

        self.canvas.grid(row = 0, column = 0, sticky = "nsew")
        vbar.grid(row = 0, column = 1, sticky = "ns")
        hbar.grid(row = 1, column = 0, sticky = "ew")

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.content.configure(width = width, height = height)


class Textbox(tkinter.Text):

    def __init__(self, parent, width):
        super().__init__(master = parent, height = 1, width = width, wrap = tkinter.NONE)
        self.bind("<Return>", lambda _: "break")


    def setVal(self, val):
        state = self.cget("state")
        self.config(state = "normal")
        self.delete("1.0", "end")
        self.insert("1.0", val)
        self.config(state = state)


    def getVal(self):
        return self.get("1.0", "end-1c")


    def setState(self, active):
        state = "normal" if active else "disabled"
        self.config(state = state)