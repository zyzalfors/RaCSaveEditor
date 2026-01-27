import tkinter
from tkinter import filedialog
from tkinter import ttk
from Checkbox import Checkbox
from Textbox import Textbox
from Combobox import Combobox
from RaCSave import RaCSave

class Form(tkinter.Tk):
    TYPES = ("bin file", "*.bin")


    def __init__(self):
        super().__init__()
        self.save = None
        self.menu = None;
        self.labels = []
        self.textboxes = []
        self.comboboxes = []
        self.checkboxes = []
        self.notebook = None
        self.initGUI()


    def initGUI(self):
        self.title("RaC Save Editor")
        self.geometry("690x720")
        self.resizable(False, False)

        menuBar = tkinter.Menu(self)
        fileMenu = tkinter.Menu(menuBar, tearoff = False)
        fileMenu.add_command(label = "Open", command = self.open)
        fileMenu.add_command(label = "Update", state = "disabled", command = self.update)
        fileMenu.add_command(label = "Close and update", state = "disabled", command = self.closeAndUpdate)
        fileMenu.add_command(label = "Close", state = "disabled", command = self.close)
        fileMenu.add_command(label = "Exit", command = self.destroy)
        menuBar.add_cascade(label = "File", menu = fileMenu)
        self.config(menu = menuBar)
        self.menu = fileMenu


    def open(self):
        path = tkinter.filedialog.askopenfilename(title = "Open", filetypes = [self.TYPES])
        if path == "":
            return

        game = tkinter.simpledialog.askstring(title = None, prompt = f"Enter game ({', '.join(RaCSave.GAMES)}):")
        if game:
            game = game.strip().lower()

        if not game in RaCSave.GAMES:
            tkinter.messagebox.showerror("Error", "Invalid game.")
            return

        self.save = RaCSave(path, game)

        chunk, check = self.save.checkCrc16()
        if chunk and not check:
            msg = "\n".join(["Invalid checksum:", f"Offset: {chunk[0]}", f"Checksum offset: {chunk[1]}", f"Data offset: {chunk[2]}", f"Data size: {chunk[3]}", "Update save to fix checksum."])
            tkinter.messagebox.showerror("Error", msg)

        self.setCommands(False)
        self.disposeTabs()
        self.initTabs()


    def update(self):
        if not self.save:
            return

        for textbox in self.textboxes:
            self.save.updateValue(textbox.name, textbox.get("1.0", tkinter.END))

        for combobox in self.comboboxes:
            self.save.updateValue(combobox.name, combobox.getVal())

        for checkbox in self.checkboxes:
            self.save.updateUnlockable(checkbox.name, bool(checkbox.isChecked()))

        self.save.update()
        tkinter.messagebox.showinfo("Info", "Save updated.")

        self.disposeTabs()
        self.initTabs()


    def closeAndUpdate(self):
        self.update()
        self.close()


    def close(self):
        self.save = None
        self.setCommands(True)
        self.disposeTabs()


    def setCommands(self, dis):
        state = "disabled" if dis else "normal"
        self.menu.entryconfig(1, state = state)
        self.menu.entryconfig(2, state = state)
        self.menu.entryconfig(3, state = state)


    def initTabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand = True, fill = "both")
        self.notebook = notebook

        valuesTab = ttk.Frame(notebook)
        notebook.add(valuesTab, text = "Values")

        label = tkinter.Label(valuesTab, text = "Path:")
        label.place(anchor = "nw", x = 0, y = 0)
        self.labels.append(label)

        textbox = Textbox(valuesTab, "path", self.save.path, True)
        textbox.place(anchor = "nw", x = 130, y = 0)
        self.textboxes.append(textbox)

        label = tkinter.Label(valuesTab, text = "Game:")
        label.place(anchor = "nw", x = 350, y = 0)
        self.labels.append(label)

        textbox = Textbox(valuesTab, "game", self.save.game, True)
        textbox.place(anchor = "nw", x = 480, y = 0)
        self.textboxes.append(textbox)

        values = self.save.getValues()
        for i in range(len(values)):
            name = values[i][0]
            val = values[i][1]

            x = 0 if i % 2 == 0 else 350
            y = 42 + 21 * i if i % 2 == 0 else 42 + 21 * (i - 1)

            label = tkinter.Label(valuesTab, text = name + ":")
            label.place(anchor = "nw", x = x, y = y)
            self.labels.append(label)

            if name == "Language":
                combobox = Combobox(valuesTab, name, val, self.save.LANGUAGES.keys())
                combobox.place(anchor = "nw", x = x + 130, y = y)
                self.comboboxes.append(combobox)

            elif name == "Armor":
                combobox = Combobox(valuesTab, name, val, self.save.ARMORS.keys())
                combobox.place(anchor = "nw", x = x + 130, y = y)
                self.comboboxes.append(combobox)

            else:
                textbox = Textbox(valuesTab, name, val, False)
                textbox.place(anchor = "nw", x = x + 130, y = y)
                self.textboxes.append(textbox)

        unlockablesTab = ttk.Frame(notebook)
        notebook.add(unlockablesTab, text = "Unlockables")

        unlockables = self.save.getUnlockables()
        for i in range(len(unlockables)):
            check = Checkbox(unlockablesTab, unlockables[i][0], unlockables[i][1])

            if i % 3 == 0:
                check.place(x = 0, y = 8 * i)

            elif i % 3 == 1:
                check.place(x = 145, y = 8 * (i - 1))

            else:
                check.place(x = 290, y = 8 * (i - 2))

            self.checkboxes.append(check)


    def disposeTabs(self):
        for label in self.labels:
            label.destroy()

        self.labels.clear()

        for textbox in self.textboxes:
            textbox.destroy()

        self.textboxes.clear()

        for combobox in self.comboboxes:
            combobox.destroy()

        self.comboboxes.clear()

        for checkbox in self.checkboxes:
            checkbox.destroy()

        self.checkboxes.clear()

        if self.notebook:
            self.notebook.destroy()