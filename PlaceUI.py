import tkinter as tk


class PlaceUI:
    def __init__(self):
        self.placement = []
        self.ui = None

    def start(self):
        self.ui = tk.Tk()
        self.ui.title("Place Me")
        self.ui.geometry("800x600")
        self.ui.mainloop()
