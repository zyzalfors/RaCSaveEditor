import tkinter
from tkinter import filedialog
from tkinter import ttk
from RaCSave import RaCSave

class Checkbox(tkinter.Checkbutton):

    def __init__(self, root, label, checked):
        self.var = tkinter.IntVar()
        self.var.set(checked)
        super().__init__(root, text = label, variable = self.var, onvalue = 1, offvalue = 0)
        self.name = label

    def isChecked(self):
        return self.var.get()

class Textbox(tkinter.Text):

    def __init__(self, root, name, x, y, val):
        super().__init__(root, height = 1, width = 16)
        self.name = name
        self.place(anchor = "nw", x = x, y = y)
        self.insert(tkinter.END, val)

class Combobox(ttk.Combobox):

    def __init__(self, root, name, x, y, val, vals):
        self.var = tkinter.StringVar()
        self.var.set(val)
        super().__init__(root, height = 1, width = 18, textvariable = self.var, state = "readonly")
        self.name = name
        self.place(anchor = "nw", x = x, y = y)
        self["values"] = tuple(vals)

    def getVal(self):
        return self.var.get()

class Form(tkinter.Tk):
    TYPES = ("bin file", "*.bin")

    def __init__(self):
        super().__init__()
        self.save = None
        self.labels = []
        self.textboxes = []
        self.langbox = None
        self.checkboxes = []
        self.initGUI()

    def initGUI(self):
        self.title("RaC Save Editor")
        self.geometry("300x700")
        self.resizable(False, False)
        menuBar = tkinter.Menu(self)
        fileMenu = tkinter.Menu(menuBar, tearoff = False)
        fileMenu.add_command(label = "Open", command = self.open)
        fileMenu.add_command(label = "Update", command = self.update)
        fileMenu.add_command(label = "Close and update", command = self.closeAndUpdate)
        fileMenu.add_command(label = "Close", command = self.close)
        fileMenu.add_command(label = "Exit", command = self.destroy)
        menuBar.add_cascade(label = "File", menu = fileMenu)
        self.config(menu = menuBar)

    def open(self):
        path = tkinter.filedialog.askopenfilename(title = "Open", filetypes = [self.TYPES])
        if path == "": return
        game = tkinter.simpledialog.askstring(title = None, prompt = "Enter game (rac1, rac2, rac3, rac4):")
        if game: game = game.strip().lower()
        if game not in RaCSave.GAMES:
            tkinter.messagebox.showerror("Error", "Invalid game")
            return
        self.save = RaCSave(path, game)
        self.disposeTab()
        self.initTab()

    def update(self):
        if not self.save: return
        for textbox in self.textboxes: self.save.updateValue(textbox.name, textbox.get("1.0", tkinter.END))
        if self.langbox: self.save.updateValue(self.langbox.name, self.langbox.getVal())
        for checkbox in self.checkboxes: self.save.updateItem(checkbox.name, bool(checkbox.isChecked()))
        self.save.update()
        tkinter.messagebox.showinfo("Info", "Save updated")

    def closeAndUpdate(self):
        self.update()
        self.save = None
        self.disposeTab()

    def close(self):
        self.save = None
        self.disposeTab()

    def initTab(self):
        shift = 0
        values = self.save.getValues()
        for value in values:
            name, val = value[0], value[1]
            label = tkinter.Label(self, text = name + ":")
            label.place(anchor = "nw", y = shift)
            self.labels.append(label)
            if name != "Language":
                textbox = Textbox(self, name, 90, shift, val)
                self.textboxes.append(textbox)
            else:
                combo = Combobox(self, name, 90, shift, val, self.save.LANGUAGES.keys())
                self.langbox = combo
            shift += 21
        items = self.save.getItems()
        for i in range(len(items)):
            check = Checkbox(self, items[i][0], items[i][1])
            if i % 2 == 0: check.place(x = 0, y = shift + 10 * i)
            else: check.place(x = 120, y = shift + 10 * (i - 1))
            self.checkboxes.append(check)

    def disposeTab(self):
        for label in self.labels: label.destroy()
        self.labels.clear()
        for textbox in self.textboxes: textbox.destroy()
        self.textboxes.clear()
        if self.langbox: self.langbox.destroy()
        self.langbox = None
        for checkbox in self.checkboxes: checkbox.destroy()
        self.checkboxes.clear()

form = Form()
form.mainloop()