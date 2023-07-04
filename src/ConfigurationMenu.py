import tkinter

from serial import SerialException
import customtkinter as ctk
from UI import *
from SerialController import *


class ConfigurationMenu(ctk.CTkTabview):

    def __init__(self, ui_frame: UI, serial_controller: SerialController):
        super().__init__(ui_frame, state="disable", segmented_button_selected_color="chartreuse4", width=240)
        # self.ui_frame = ui_frame
        self.baud_var = tkinter.IntVar(value=115200)
        self.mode = tkinter.StringVar(value="Normal Mode")
        self.serial_controller = serial_controller

        self._menu_setup()

    def _set_mode(self):
        if self.switch.get() == 0:
            return

        self.serial_controller.set_mode(self.mode.get()[0])

    def _menu_setup(self):
        self.add("CONFIGURATION")
        self.tab("CONFIGURATION").grid_columnconfigure(0, weight=1)
        self._configuration_frame()

    def _baud_frame_setup(self):
        baud_frame = ctk.CTkFrame(self.tab("CONFIGURATION"))
        baud_frame.grid(row=1, column=0, padx=(20, 20), pady=(5, 0), sticky="nwse")
        # baud_frame.grid_columnconfigure(0, weight=1)

        available_baud = ((115200, "115200  bit/s", (10, 5)), (9600, "9600  bit/s    ", (5, 10)))

        for baud_tuple in available_baud:
            ctk.CTkRadioButton(baud_frame, variable=self.baud_var, value=baud_tuple[0], text=baud_tuple[1]).grid(row=available_baud.index(baud_tuple), column=0, pady=baud_tuple[2], padx=10)

    def _mode_frame_setup(self):
        mode_frame = ctk.CTkFrame(self.tab("CONFIGURATION"))
        mode_frame.grid(row=2, column=0, padx=(20, 20), pady=(5, 0), sticky="nwse")
        # mode_frame.grid_columnconfigure(0, weight=1)

        available_mode = (("Normal Mode     ", (10, 5)), ("Sleep Mode        ", (5, 5)), ("Balancing Mode", (5, 10)))

        for mode in available_mode:
            ctk.CTkRadioButton(mode_frame, variable=self.mode, value=mode[0].strip(), text=mode[0], command=self._set_mode).grid(row=available_mode.index(mode), column=0, pady=mode[1], padx=10)

    def _appearance_frame_setup(self):
        appearance_frame = ctk.CTkFrame(self)
        appearance_frame.grid(row=7, column=0, pady=(20, 0), sticky="nsew")
        appearance_frame.grid_columnconfigure(0, weight=1)
        option = ctk.CTkOptionMenu(appearance_frame, values=["Dark", "Light", "System"], command=lambda app_mode: ctk.set_appearance_mode(app_mode))
        option.grid(pady=(8, 8))

    def _get_com(self):
        connected = get_com()
        if len(connected) == 0:
            connected = ["No Device Found"]
            self.switch.deselect()
        self.option_COM.configure(values=connected)
        self.option_COM.set(connected[0])

    def _switch_event(self):
        if self.switch.get() == 0:
            self.serial_controller.close()
        else:
            if self.option_COM.get() == "No Device Found":
                self.switch.deselect()
                self.textbox.configure(text="Select a correct Serial Port")
            else:
                try:
                    self.serial_controller.open(self.baud_var.get(), self.option_COM.get())
                except SerialException:
                    self.switch.deselect()
                    self._get_com()
                    self.textbox.configure(text="Not possible to open that port, please select another one")

    def _configuration_frame(self):

        self.option_COM = ctk.CTkOptionMenu(self.tab("CONFIGURATION"))
        self._get_com()
        self.option_COM.grid(row=0, column=0, padx=20, pady=(15, 5))

        self._baud_frame_setup()
        self._mode_frame_setup()

        self.switch = ctk.CTkSwitch(self.tab("CONFIGURATION"), text=f"OFF/ON", command=self._switch_event, switch_width=60, switch_height=30)
        self.switch.grid(row=3, column=0, padx=20, pady=(30, 10))

        buttons = (("Refresh Serial", (15, 5)), ("Reset Serial", (5, 15)))
        for button in buttons:
            tkButton = ctk.CTkButton(self.tab("CONFIGURATION"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text=button[0], command=None)
            tkButton.grid(row=buttons.index(button) + 4, column=0, padx=(20, 20), pady=button[1], sticky="nwse")

        self.textbox = ctk.CTkLabel(self, height=100, fg_color=("gray70", "gray10"), corner_radius=5, text="Select the settings and press ON")
        self.textbox.grid(row=6, column=0, pady=(10, 0), sticky="nsew")

        self._appearance_frame_setup()
