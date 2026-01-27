import tkinter

class Textbox(tkinter.Text):

    def __init__(self, root, name, val, dis):
        super().__init__(root, height = 1, width = 25, wrap = tkinter.NONE)
        self.name = name
        self.insert(tkinter.END, val)
        self.bind("<Return>", lambda _: "break")

        if dis:
            self.config(state = "disabled")