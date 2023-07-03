import tkinter
import customtkinter as ctk
from UI import *


class ConfigurationMenu(ctk.CTkTabview):

    def __init__(self, ui_frame: UI):
        super().__init__(ui_frame, state="disable", segmented_button_selected_color="chartreuse4", width=240)
        # self.ui_frame = ui_frame
        self.baud_var = tkinter.IntVar(value=115200)

        self._menu_setup()



    def _menu_setup(self):
        self.add("CONFIGURATION")
        self.tab("CONFIGURATION").grid_columnconfigure(0, weight=1)
        self.configuration_frame()

    def _baud_frame_setup(self):
        baud_frame = ctk.CTkFrame(self.tab("CONFIGURATION"))
        baud_frame.grid(row=1, column=0, padx=(20, 20), pady=(5, 0), sticky="nwse")
        # baud_frame.grid_columnconfigure(0, weight=1)

        available_baud = ((115200, "115200  bit/s"), (9600, "9600  bit/s    "))

        for baud_tuple in available_baud:
            ctk.CTkRadioButton(baud_frame, variable=self.baud_var, value=baud_tuple[0], text=baud_tuple[1]).grid(row=available_baud.index(baud_tuple), column=0, pady=(10, 10), padx=10)


    def configuration_frame(self):

        self.option_COM = ctk.CTkOptionMenu(self.tab("CONFIGURATION"))
        # self.get_COM()
        self.option_COM.grid(row=0, column=0, padx=20, pady=(15, 5))

        self._baud_frame_setup()

        self.switch = ctk.CTkSwitch(self.tab("CONFIGURATION"), text=f"OFF/ON", command=None, switch_width=60, switch_height=30)
        self.switch.grid(row=3, column=0, padx=20, pady=(30, 10))








        mode_frame = ctk.CTkFrame(self.tab("CONFIGURATION"))
        mode_frame.grid(row=2, column=0, padx=(20, 20), pady=(5, 0), sticky="nwse")
        # mode_frame.grid_columnconfigure(0, weight=1)

        self.mode = tkinter.StringVar(value="Normal Mode")
        normal = ctk.CTkRadioButton(master=mode_frame, variable=self.mode, value="Normal Mode", text="Normal Mode     ", command=None)
        normal.grid(row=1, column=0, pady=(10, 5))
        silent = ctk.CTkRadioButton(master=mode_frame, variable=self.mode, value="Sleep Mode", text="Sleep Mode        ", command=None)
        silent.grid(row=2, column=0, pady=(5, 5))
        balancing = ctk.CTkRadioButton(master=mode_frame, variable=self.mode, value="Balancing Mode", text="Balancing Mode", command=None)
        balancing.grid(row=3, column=0, pady=(5, 10))

        refresh = ctk.CTkButton(self.tab("CONFIGURATION"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Refresh Serial",
                                command=None)
        refresh.grid(row=4, column=0, padx=(20, 20), pady=(15, 5), sticky="nwse")
        reset = ctk.CTkButton(self.tab("CONFIGURATION"), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Reset Serial",
                              command=None)
        reset.grid(row=5, column=0, padx=(20, 20), pady=(5, 15), sticky="nwse")

        # create textbox
        self.textbox = ctk.CTkLabel(self, height=100, fg_color=("gray70", "gray10"), corner_radius=5)
        self.textbox.grid(row=6, column=0, pady=(10, 0), sticky="nsew")

        # appearance frame
        appearance_frame = ctk.CTkFrame(self)
        appearance_frame.grid(row=7, column=0, pady=(20, 0), sticky="nsew")
        appearance_frame.grid_columnconfigure(0, weight=1)
        option = ctk.CTkOptionMenu(appearance_frame, values=["Dark", "Light", "System"], command=None)
        option.grid(pady=(8, 8))
