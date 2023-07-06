from Slave import *
import customtkinter as ctk
from Constants import *
from SummaryInfo import *
from struct import *


class DataFrame(ctk.CTkFrame):

    def __init__(self, ui_frame):
        super().__init__(ui_frame)

        self.slaves = list()
        self._setup_slaves_frame()
        self.ui_frame = ui_frame

        self.summary_info = SummaryInfo(self)
        self.summary_info.grid(row=1, column=0, padx=(10, 10), pady=(20, 5), sticky="nsew", columnspan=N_SLAVES + 1)

        self.mode_function = {
            "Normal Mode": self._update_gui_normal,
            "Sleep Mode": self._update_gui_sleep,
            "Balancing Mode": self._update_gui_balancing
        }

        self._update_gui()

    def _setup_slaves_frame(self) -> None:
        index_frame = get_index_frame(self)
        index_frame.grid(column=0, row=0, sticky="nsew")

        for i in range(0, N_SLAVES):
            slave = Slave(self, i)
            slave.grid(column=i + 1, row=0, padx=(5, 5 if i == N_SLAVES - 1 else 0), sticky="nsew")
            self.slaves.append(slave)

    def _get_switch(self) -> int:
        return self.ui_frame.menu.get_switch()

    def _get_mode(self) -> str:
        return self.ui_frame.menu.get_mode()

    def _get_text(self) -> str:
        return self.ui_frame.menu.get_text()

    def _set_text(self, message: str) -> None:
        self.ui_frame.menu.set_text(message)

    def _update_gui(self) -> None:

        if self._get_switch() == 1:
            self.mode_function[self._get_mode()]()

        self.after(UPDATE_FREQ, self._update_gui)

    def _update_gui_normal(self) -> None:
        try:
            packet = self.ui_frame.serial_controller.read_packet()
            self._update_logic(packet)
        except TimeoutError:
            self.ui_frame.menu.error_serial("Device not responding, retry or select another port")
        except TypeError:
            self.ui_frame.menu.error_serial("Device not responding, probably disconnected")
        except struct.error:
            self.ui_frame.menu.error_serial("Error Unpacking")  # probably host has changed the struct definition

    def _update_gui_sleep(self) -> None:
        for i in range(N_SLAVES):
            self.slaves[i].update_slave([0] * (N_VS + N_TS), 0, 0)
        self.summary_info.update_info([0] * 9)

    def _update_gui_balancing(self) -> None:
        self._update_gui_normal()

    def _update_logic(self, packet: bytes) -> None:

        # max_volt;  min_volt; tot_volt; max_temp; min_temp; tot_temp; max_temp_slave;
        minmax = list(unpack(FORMAT_MIN_MAX, packet[size_slave * N_SLAVES: size_slave * N_SLAVES + size_minmax]))
        alive_slaves = self._update_slaves(packet, minmax[0], minmax[1])

        self._update_infos(packet, minmax, alive_slaves)

    def _update_slaves(self, packet: bytes, max_volt: float, min_volt: float) -> int:

        alive_slaves = 0
        for i in range(N_SLAVES):
            cell_value = unpack(FORMAT_SLAVE, packet[i * size_slave: (i + 1) * size_slave])
            alive_slaves += self.slaves[i].update_slave(cell_value, max_volt, min_volt)

        return alive_slaves

    def _update_infos(self, packet: bytes, minmax: list, alive_slaves: int):
        # curr;   last_recv;
        lem = list(unpack(FORMAT_LEM, packet[size_slave * N_SLAVES + size_minmax + size_fan: size_slave * N_SLAVES + size_minmax + size_fan + size_lem]))

        minmax.pop()  # remove which slave has the max temp
        if alive_slaves != 0:
            minmax[5] /= (alive_slaves * N_TS)  # from tot temp to avg temp
            minmax.insert(3, minmax[2] / (alive_slaves * N_VS))  # add avg voltage
        else:
            minmax[5] = 0
            minmax.insert(3, 0)

        minmax.append(lem[0] / 1000.0)  # add current
        minmax.append((lem[0] / 1000.0) * minmax[2])  # add power

        for i in range(4):
            minmax[i] /= 10000

        self.summary_info.update_info(minmax)


# return the index frame of the slaves table
def get_index_frame(master: DataFrame) -> ctk.CTkFrame:
    index_frame = ctk.CTkFrame(master)
    label = ctk.CTkLabel(index_frame, text="", fg_color="transparent", corner_radius=4, width=52)
    label.grid(column=0, row=0, sticky="nsew", pady=(17, 5), padx=(5, 5))

    for i in range(0, N_VS + N_TS):
        label = ctk.CTkLabel(index_frame, text="Cell " + str(i + 1) if i < N_VS else "Tmp " + str(i - N_VS + 1), fg_color=("gray70", "gray25"), corner_radius=4, width=52)
        label.grid(column=0, row=i + 1, sticky="nsew", pady=(5, 5), padx=(5, 5))

    return index_frame
