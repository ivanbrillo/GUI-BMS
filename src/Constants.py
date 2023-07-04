import struct

N_VS = 9
N_TS = 3
N_SLAVES = 16

UPDATE_FREQ = 300
MIN_ERR = 30

# H -> half_word (2 Byte),  ? -> bool (1 Byte),  c -> char (1 Byte), I -> Unsigned int  B -> uint8, x -> pad byte
# https://docs.python.org/3/library/struct.html
# pay attention to the struct alignment in Host code!

# uint16_t volts[]; int16_t temps[];  uint8_t addr;  uint8_t err;
FORMAT_SLAVE = "H" * (N_VS + N_TS) + "BB"
size_slave = struct.calcsize(FORMAT_SLAVE)

# uint16_t max_volt;  uint16_t min_volt;  uint32_t tot_volt;  uint16_t max_temp; uint16_t min_temp;  uint16_t tot_temp;  uint8_t max_temp_slave;
FORMAT_MIN_MAX = "H" * 2 + "I" + "H" * 3 + "Bx"
size_minmax = struct.calcsize(FORMAT_MIN_MAX)

# uint16_t prev_temp; bool on;
FORMAT_FAN = "H?x"
size_fan = struct.calcsize(FORMAT_FAN)

# uint32_t curr;  uint32_t last_recv;
FORMAT_LEM = "I" * 2
size_lem = struct.calcsize(FORMAT_LEM)

#   bool sdc_closed;  uint32_t fault_volt_tmstp;  uint32_t fault_temp_tmstp;  Mode mode (int 32 bit);
FORMAT_ADDITIONAL_INFO = "?xxx" + "I" * 2 + "i"
size_additional_info = struct.calcsize(FORMAT_ADDITIONAL_INFO)

#   float bus_volt;  bool via_can;  uint32_t start_tmstp;  uint8_t cycle_counter;  bool done;
FORMAT_PRECHARGE = "f?xxxIB?xx"
size_precharge = struct.calcsize(FORMAT_PRECHARGE)

FORMAT_PAYLOAD = FORMAT_SLAVE * N_SLAVES + FORMAT_MIN_MAX + FORMAT_FAN + FORMAT_LEM + FORMAT_ADDITIONAL_INFO + FORMAT_PRECHARGE + "?xxx"  # +computer connected and padding
size_payload = struct.calcsize(FORMAT_PAYLOAD)

# print("SLAVE:" + str(size_slave))
# print("PRECHARGE:" + str(struct.calcsize(FORMAT_PRECHARGE)))
# print("LEM:" + str(size_lem))
# print("ADD:" + str(struct.calcsize(FORMAT_ADDITIONAL_INFO)))
# print("TOT:" + str(size_payload))
