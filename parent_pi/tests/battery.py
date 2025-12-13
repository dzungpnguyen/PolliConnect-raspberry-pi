from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2


# def read():
#     ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
#     ina.configure(ina.RANGE_16V)

#     print("Bus Voltage: %.3f V" % ina.voltage())
#     try:
#         print("Bus Current: %.3f mA" % ina.current())
#         print("Power: %.3f mW" % ina.power())
#         print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
#     except DeviceRangeError as e:
#         # Current out of device range with specified shunt resistor
#         print(e)

def read():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    read()

# Since IN219 cannot directly get the level of charge of Raspberry Pi, we can roughly estimate from the voltage of the battery
def estimate_charge_level(current_voltage, battery_capacity):
    current_charge_level = None
    current_capacity = None
    full_charge_voltage = 4.1
    no_charge_voltage = 3
    delta_voltage = full_charge_voltage - no_charge_voltage
    try:
        if 3 <= current_voltage <= 4.1:
            current_charge_level = (current_voltage - no_charge_voltage) / delta_voltage
            current_capacity = battery_capacity * current_charge_level
        else:
            print("Current voltage out of range!")
    except:
        print("Current voltage not found!")
    return current_charge_level, current_capacity


def estimate_remaing_time(current, current_capacity):
    remaing_time = None
    try:
        remaing_time = current_capacity / current
    except:
        return ValueError
    return remaing_time


if __name__ == "__main__":
    read()
