from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

from SerialController import *
from ConfigurationMenu import *
from Constants import *
import customtkinter as ctk
from Slave import *


class UI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("BMS UI")
        # self.resizable(False, False)
        self.geometry("+20+20")  # top left corner

        self.serial_controller = SerialController()
        self.menu = ConfigurationMenu(self, self.serial_controller)
        self.menu.grid(row=0, column=0, padx=(20, 20))

        slave_box = ctk.CTkFrame(self)
        slave_box.grid(row=0, column=1, padx=(10, 10), pady=(20, 20), sticky="nsew", rowspan=2, ipadx=3)
        slave_box.rowconfigure(0, weight=1)

        index_frame = get_index_frame(slave_box)
        index_frame.grid(column=0, row=0)

        for i in range(0, N_SLAVES):
            slave = Slave(slave_box, i)
            slave.grid(column=i + 1, row=0, padx=(5, 5 if i == N_SLAVES - 1 else 0))

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
    # app.geometry("1800x800")
    app.iconbitmap("icon.ico")

    # app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
