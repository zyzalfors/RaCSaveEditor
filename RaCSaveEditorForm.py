import tkinter
from tkinter import filedialog, messagebox, simpledialog, ttk
from widgets import Checkbox, Combobox, Tab, Textbox
from RaCSave import RaCSave

class RaCSaveEditorForm(tkinter.Tk):
    TYPES = ("bin file", "*.bin")


    def __init__(self, path):
        super().__init__()
        self.save = None
        self.initGUI()
        self.open(path, False)


    def initGUI(self):
        self.title("RaC Save Editor")
        self.notebook = None
        self.initMenu()
        self.geometry("790x720")
        self.protocol("WM_DELETE_WINDOW", self.onClose)


    def onClose(self):
        if self.save is not None:
            if not self.askConfirmForLoadedSave(): return

        self.destroy()


    def initMenu(self):
        menuBar = tkinter.Menu(self)

        fileMenu = tkinter.Menu(menuBar, tearoff = False)
        fileMenu.add_command(label = "Open", command = lambda: self.open(None, True))
        fileMenu.add_command(label = "Update", state = "disabled", command = self.update)
        fileMenu.add_command(label = "Close", state = "disabled", command = self.close)
        self.fileMenu = fileMenu

        shortcutMenu = tkinter.Menu(menuBar, tearoff = False)
        shortcutMenu.add_command(label = "All unlockables", state = "disabled", command = self.setAllUnlockables)
        self.shortcutMenu = shortcutMenu

        menuBar.add_cascade(label = "File", menu = fileMenu)
        menuBar.add_cascade(label = "Shortcut", menu = shortcutMenu)
        self.config(menu = menuBar)


    def open(self, path, ask):
        if ask: path = filedialog.askopenfilename(title = "Open save", filetypes = [self.TYPES])
        if not path: return

        if self.save is not None:
            if not self.askConfirmForLoadedSave(): return

        game = simpledialog.askstring(title = None, prompt = f"Enter game ({', '.join(RaCSave.GAMES)}):")
        if game: game = game.strip().lower()

        if game not in RaCSave.GAMES:
            messagebox.showerror("Error", "Invalid game")
            return

        try:
            self.data = {}
            self.save = RaCSave(path, game)

            chunk, valid = self.save.validCrc16()
            if chunk and not valid:
                msg = f"Invalid checksum:\nOffset: {chunk[0]}\nChecksum offset: {chunk[1]}\nData offset: {chunk[2]}\nData size: {chunk[3]}"
                messagebox.showinfo("Info", msg)

            self.setCommands(False)
            self.disposeTabs()
            self.initTabs()

        except Exception as e:
            self.data = {}
            self.save = None
            self.setCommands(True)
            self.disposeTabs()
            messagebox.showerror("Error", str(e))


    def update(self):
        if self.save is None: return

        try:
            for name in self.data:
                if isinstance(self.data[name], Textbox) or isinstance(self.data[name], Combobox):
                    self.save.updateValue(name, self.data[name].getVal())

                elif isinstance(self.data[name], Checkbox):
                    self.save.updateUnlockable(name, self.data[name].getVal())

            self.save.update()
            messagebox.showinfo("Info", "Save updated")
            return True

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False


    def close(self):
        if self.update():
            self.setCommands(True)
            self.disposeTabs()
            self.save = None


    def setCommands(self, dis):
        state = "disabled" if dis else "normal"
        self.fileMenu.entryconfig(1, state = state)
        self.fileMenu.entryconfig(2, state = state)
        self.fileMenu.entryconfig(3, state = state)
        self.shortcutMenu.entryconfig(1, state = state)


    def askConfirmForLoadedSave(self):
        res = messagebox.askyesnocancel("Confirmation", "Update current save?")

        match res:
            case None:
                return False

            case True:
                return self.update()

        return True


    def initTabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand = True, fill = "both")
        self.initValuesTab()
        self.initUnlockablesTab()


    def initValuesTab(self):
        tab = Tab(self.notebook, 720, 730)
        self.notebook.add(tab, text = "Values")

        deltaText = 165
        deltaLabel = 380

        label = tkinter.Label(tab.content, text = "Path:")
        label.place(x = 0, y = 0)

        text = Textbox(tab.content, 20)
        text.place(x = deltaText, y = 0)
        text.setState(False)
        text.setVal(self.save.path)

        label = tkinter.Label(tab.content, text = "Game:")
        label.place(x = deltaLabel, y = 0)

        text = Textbox(tab.content, 20)
        text.place(x = deltaText + deltaLabel, y = 0)
        text.setState(False)
        text.setVal(self.save.game)

        values = self.save.getValues()
        for i in range(len(values)):
            name, val = values[i][0], values[i][1]

            x = 0 if i % 2 == 0 else deltaLabel
            y = 42 + 21 * i if i % 2 == 0 else 42 + 21 * (i - 1)

            label = tkinter.Label(tab.content, text = f"{name}:")
            label.place(x = x, y = y)

            if name == "Level":
                combo = Combobox(tab.content, tuple(self.save.LEVELS[self.save.game].keys()), 24)
                combo.place(x = x + deltaText, y = y)
                combo.setVal(val)
                self.data[name] = combo

            elif name == "Language":
                combo = Combobox(tab.content, tuple(self.save.LANGUAGES.keys()), 24)
                combo.place(x = x + deltaText, y = y)
                combo.setVal(val)
                self.data[name] = combo

            elif name == "Armor":
                combo = Combobox(tab.content, tuple(self.save.ARMORS.keys()), 24)
                combo.place(x = x + deltaText, y = y)
                combo.setVal(val)
                self.data[name] = combo

            else:
                text = Textbox(tab.content, 20)
                text.place(x = x + deltaText, y = y)
                text.setVal(val)
                self.data[name] = text


    def initUnlockablesTab(self):
        tab = Tab(self.notebook, 720, 1050)
        self.notebook.add(tab, text = "Unlockables")

        unlockables = self.save.getUnlockables()
        for i in range(len(unlockables)):
            name, val = unlockables[i][0], unlockables[i][1]

            check = Checkbox(tab.content, name)
            check.setVal(val)
            self.data[name] = check

            col = i % 5
            row = i // 5
            check.place(x = 145 * col, y = 30 * row)


    def setAllUnlockables(self):
        for name in self.data:
            if isinstance(self.data[name], Checkbox):
                self.data[name].setVal(True)


    def disposeTabs(self):
        if self.notebook:
            self.notebook.destroy()
            self.notebook = None