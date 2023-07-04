from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

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

        self.serial_controller = SerialController()
        self.menu = ConfigurationMenu(self, self.serial_controller)
        self.menu.grid(row=0, column=0, padx=(20, 20))

    # try:
    #     dataIn = self.port.read()
    # except serial.SerialException as e:
    #     # There is no new data from serial port
    #     return None
    # except TypeError as e:
    #     # Disconnect of USB->UART occured
    #     self.port.close()
    #     return None
    # else:
    #     # Some data was received
    #     return dataIn

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
    app.geometry("1800x800")
    app.iconbitmap("icon.ico")

    # app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
