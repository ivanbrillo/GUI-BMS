from Slave import *
import customtkinter as ctk
from Constants import *


class Slaves(ctk.CTkFrame):

    def __init__(self, ui_frame):
        super().__init__(ui_frame)

        self.slaves = list()
        self._setup_slaves_frame()
        # self._update_gui()

    def _setup_slaves_frame(self):
        index_frame = get_index_frame(self)
        index_frame.grid(column=0, row=0, sticky="nsew", rowspan=3)

        for i in range(0, N_SLAVES):
            slave = Slave(self, i)
            slave.grid(column=i + 1, row=0, padx=(5, 5 if i == N_SLAVES - 1 else 0), sticky="nsew")
            self.slaves.append(slave)

    # def _update_gui(self):
    #
    #
    #
    #     if self.switch.get() == 0:
    #         if self.textbox.cget("text") != "Select a correct Serial Port":
    #             self.textbox.configure(text="Select the settings and press ON")
    #
    #     else:
    #         self.textbox.configure(text="Selected port is ON and listen")
    #         if self.mode.get() == "Normal Mode":
    #             self.update_gui_normal()
    #         elif self.mode.get() == "Sleep Mode":
    #             self.update_silent()
    #         else:
    #             self.update_bilancing()
    #
    #     self.after(UPDATE_FREQ, self._update_gui)




    # try:
    #     dataIn = self.port.read()
    # except serial.SerialException as e:
    #     # There is no new data from serial port
    #     return None
    # except TypeError as e:
    #     # Disconnect of USB->UART occurred
    #     self.port.close()
    #     return None
    # else:
    #     # Some data was received
    #     return dataIn
