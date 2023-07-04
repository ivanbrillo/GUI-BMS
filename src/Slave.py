import customtkinter as ctk
from UI import *
from Constants import *


def volt_rgb(value):
    if 3.5 <= value < 4.2:
        return "green"
    elif 3.4 <= value < 3.5:
        return "yellow"
    else:
        return "red"


def temp_rgb(value):
    if 0 <= value < 20:
        return "blue"
    if 20 <= value < 50:
        return "green"
    elif 50 <= value < 60:
        return "yellow"
    else:
        return "red"


class Slave(ctk.CTkFrame):

    rgb_function = {
        "volt": lambda value: volt_rgb(value),
        "temp": lambda value: temp_rgb(value)
    }

    def __init__(self, master, number_slv: int):
        super().__init__(master, fg_color="transparent")
        self.number_slv = number_slv
        self.values = list()
        self._create_slave()

    def _create_slave(self):
        select_slv = ctk.CTkCheckBox(self, text="Slv " + str(self.number_slv), fg_color=("gray70", "gray25"), corner_radius=4, width=70)
        select_slv.configure(command=lambda: self._deselect_slave(select_slv))
        select_slv.select()
        select_slv.grid(column=0, row=0, sticky="nsew", padx=(5, 5), pady=(20, 5))

        for j in range(1, N_VS + N_TS + 1):
            label = ctk.CTkLabel(self, text="0", fg_color=("gray80", "gray15"), corner_radius=4, text_color="black", font=("sans-serif", 14))
            label.grid(column=0, row=j, sticky="nsew", padx=(2, 2), pady=(5, 5))
            self.values.append(label)

    def _deselect_slave(self, button):
        if button.get() == 0:
            for e in self.values:
                e.grid_forget()
        else:
            for i, e in enumerate(self.values):
                e.grid(column=0, row=i + 1, sticky="nsew", padx=(2, 2), pady=(5, 5))

    # Return true if the slave is dead, false if it's not
    def update_slave(self, list_values: list, max_volt: float, min_volt: float) -> int:

        value_style = {
            max_volt: (("sans-serif", 14, "bold"), "blue"),
            min_volt: (("sans-serif", 14, "bold"), "cyan")
        }

        if list_values[N_VS + N_TS + 1] > MIN_ERR:
            for j in range(N_VS + N_TS):
                self.values[j].configure(text="DEAD", fg_color="black", text_color="white")
            return 0

        elif list_values[N_VS + N_TS + 1] != 0:
            for j in range(N_VS + N_TS):
                self.values[j].configure(text="ERR", fg_color="gray", text_color="black")
            return 0

        else:
            for j in range(N_VS):
                style = value_style.get(list_values[j], (("sans-serif", 14), "black"))
                value = round(list_values[j] / 10000, 3)
                self.values[j].configure(text=str(value), fg_color=Slave.rgb_function["volt"](value), text_color=style[1], font=style[0])

            for j in range(N_VS, N_VS + N_TS):
                value = round(list_values[j], 2)
                self.values[j].configure(text=str(value), fg_color=Slave.rgb_function["temp"](value), font=("sans-serif", 14), text_color="black")

        return 1
