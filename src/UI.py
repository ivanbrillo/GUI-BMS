
from SerialController import *
from ConfigurationMenu import *
from Constants import *
import customtkinter as ctk


class UI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("BMS UI")
        # self.resizable(False, False)
        self.geometry("+20+20")  # top left corner

        self.SerialController = SerialController()
        self.menu = ConfigurationMenu(self)

        self.menu.grid(row=0, column=0, padx=(20, 20))




    #
    #     self.update_gui()
    #
    # def update_gui(self):
    #
    #
    #
    #
    #     self.after(UPDATE_FREQ, self.update_gui)
    #

if __name__ == "__main__":
    app = UI()
    # app.geometry("1800x800")

    # app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
