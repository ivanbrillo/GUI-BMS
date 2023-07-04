import customtkinter as ctk
from UI import *
from Constants import *


def get_index_frame(master) -> ctk.CTkFrame:
    index_frame = ctk.CTkFrame(master)
    label = ctk.CTkLabel(index_frame, text="", fg_color="transparent", corner_radius=4, width=52)
    label.grid(column=0, row=0, sticky="nsew", pady=(17, 5), padx=(5, 5))

    for i in range(0, N_VS + N_TS):
        label = ctk.CTkLabel(index_frame, text="Cell " + str(i + 1) if i < N_VS else "Tmp " + str(i - N_VS + 1), fg_color=("gray70", "gray25"), corner_radius=4, width=52)
        label.grid(column=0, row=i + 1, sticky="nsew", pady=(5, 5), padx=(5, 5))

    return index_frame


class Slave(ctk.CTkFrame):

    def __init__(self, master, number_slv: int):
        super().__init__(master)
        self.number_slv = number_slv
        self.values = list()
        self._create_slave()

    def _create_slave(self):
        select_slv = ctk.CTkCheckBox(self, text="Slv " + str(self.number_slv), fg_color=("gray70", "gray25"), corner_radius=4, width=70)
        select_slv.configure(command=lambda: self._deselect_slave(select_slv))
        select_slv.select()
        select_slv.grid(column=0, row=0, sticky="nsew", padx=(5, 5), pady=(20, 5))

        for j in range(1, N_VS + N_TS + 1):
            label = ctk.CTkLabel(self, text="0", fg_color=("gray80", "gray15"), corner_radius=4, text_color="black")
            label.grid(column=0, row=j, sticky="nsew", padx=(2, 2), pady=(5, 5))
            self.values.append(label)

    def _deselect_slave(self, button):
        if button.get() == 0:
            for e in self.values:
                e.grid_forget()
        else:
            for i, e in enumerate(self.values):
                e.grid(column=0, row=i + 1, sticky="nsew", padx=(2, 2), pady=(5, 5))
