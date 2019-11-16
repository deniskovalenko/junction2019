import requests
import sys
import os
import datetime, time
import decimal
import serial
import serial.tools.list_ports
from datetime import datetime
import uuid

# Light level values in percentage (0 no light, 100 full brightness)
LIGHT_LEVEL_ARRAY = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 52, 55, 58, 60, 63, 65, 68, 70, 73, 75, 78, 80, 82, 85,
                     88, 90, 93, 95, 98, 100]
# Mapped values of brigthness in DALI (light control protocol) commands HEX values
DALI_LIGHT_LEVEL_HEX_ARRAY = ["00", "90", "AA", "B9", "C4", "CB", "D2", "D8", "DD", "E1", "E5", "E6", "E8", "EA", "EB",
                              "ED", "EE", "F0", "F1", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "FA", "FB", "FC", "FD",
                              "FE"]

# Color temperature in Kelvin, 6500K is the coolest temperature, 2700K is the warmest
COLOUR_TEMPERATURE_ARRAY = [6500, 6400, 6300, 6200, 6100, 6000, 5900, 5800, 5700, 5600, 5500, 5400, 5300, 5200, 5100,
                            5000, 4900, 4800, 4700, 4600, 4500, 4400, 4300, 4200, 4100, 4000, 3900, 3800, 3700, 3600,
                            3500, 3400, 3300, 3200, 3100, 3000, 2900, 2800, 2700]
# Mapped values of color temperature to in HEX
COLOUR_TEMPERATURE_HEX_ARRAY = ["1964", "1900", "189C", "1838", "17D4", "1770", "170c", "16A8", "1644", "15E0", "157C",
                                "1518", "14B4", "1450", "13EC", "1388", "1324", "12C0", "125C", "11F8", "1194", "1130",
                                "10CC", "1068", "1004", "0FA0", "0F3C", "0ED8", "0E74", "0E10", "0DAC", "0D48", "0CE4",
                                "0C80", "0C1C", "0BB8", "0B54", "0AF0", "0A8C"]

# LUMINAIRE_ID = "EC22" #Example A1B3

# "00" - manual mode, you are in full controll of luminaire, PIR is off
# "01" - automatic , mode PIR sensor is in use, luminaire goes on when triggered and off after occupancy timeout
LUMIAIRE_MODE = "00"


class LightControlService(object):

    def __init__(self, config):
        self.config = config
        Port_name = self.get_serial_port()
        if Port_name:
            # port Exists so init it
            self.Serial_Device = self.init_serial_port(Port_name)

    # in memoru non-thread-safe cache for current state of light system
    cache = {}

    def get_state(self):
        return self.cache

    '''
        Updates lamp status without logging it
        structure:
        device_id
        light_level_value
        color_temperature_value
        '''

    def update_light(self, light_settings):
        device_id = light_settings["device_id"]
        new_settings = light_settings["settings"]
        light_level_value = new_settings["light_level_value"]
        color_temperature_value = new_settings["color_temperature_value"]

        self.update_light_settings(device_id, light_level_value, color_temperature_value)
        return "OK"

    '''
    Sets new state and logs request to DB
    structure:
    device_id
    light_level_value
    color_temperature_value
    '''

    def set_light(self, light_settings):
        device_id = light_settings["device_id"]
        new_settings = light_settings["settings"]
        light_level_value = new_settings["light_level_value"]
        color_temperature_value = new_settings["color_temperature_value"]
        previous_state = None
        if device_id in self.cache:
            previous_state = self.cache[device_id]
            if previous_state["settings"] == new_settings:
                not_updated_msg = "state didn't change, not updating"
                print(not_updated_msg)
                return not_updated_msg

        settings_to_save = {"device_id": device_id, "settings": new_settings, "id": str(uuid.uuid4())}
        self.cache[device_id] = settings_to_save

        self.update_light_settings(device_id, light_level_value, color_temperature_value)
        self.log_update(device_id, previous_state, settings_to_save)
        return "OK"


    def update_light_settings(self, device_id, light_level_value, color_temperature_value):
        self.set_light_level_color_temperature(device_id,
                                               self.Serial_Device,
                                               light_level_value,
                                               color_temperature_value)

    def log_update(self, device_id, previous_state, new_settings):
        log_object = {"id": new_settings["id"],
                      "device_id": device_id,
                      "location": "meeting_room_hq13-2",
                      "user": "denisk",
                      "timestamp": datetime.now().isoformat(),
                      "previous_state": previous_state,
                      "settings": new_settings["settings"]}
        print(log_object)

    def init_serial_port(self, _port):
        if not _port:
            print('No port number supplied')
            return None
        else:
            try:
                serialDevice = serial.Serial(_port)
                serialDevice.baudrate = 115200
                serialDevice.bytesize = serial.EIGHTBITS
                serialDevice.parity = serial.PARITY_NONE
                serialDevice.stopbits = serial.STOPBITS_ONE
                serialDevice.timeout = 0
                serialDevice.xonxoff = False
                serialDevice.rtscts = False
                serialDevice.dsrdtr = False
                return serialDevice
            except (ValueError, IOError, Exception) as ex:
                print("error init serial port: " + str(ex))
                return None

    def get_serial_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # This is for debugging Enable if you want to see what arte the devices connected
            # print('device: ', p.device, 'manufacturer: ', p.manufacturer, 'description: ', p.description, p.hwid )
            if p.manufacturer and 'FTDI' in p.manufacturer:
                if p.description and ('USB Serial Port' in p.description or 'TTL232R-3V3' in p.description):
                    return p.device

            if p.manufacturer and 'FTDI' in p.manufacturer or 'TTL232R-3V3' in p.description:
                # Enable if you want to see debug msg if the device found
                # print( 'found it', p.manufacturer)
                return p.device
        return None

    def set_light_level_color_temperature(self, device_id, _serialDevice, _lightLevelValue=50, _colourTemperatureValue=3900):
        if not _serialDevice.isOpen():
            try:
                # uncomment for debugging
                # print('Serial device is not open, trying to open it')
                _serialDevice.open()
            except (ValueError, IOError) as ex:
                # uncomment for debugging
                # print("error opening serial port: " + str(ex))
                return None

        if _serialDevice.isOpen():
            try:
                ser = _serialDevice
                lightValIndex = min(range(len(LIGHT_LEVEL_ARRAY)),
                                    key=lambda i: abs(LIGHT_LEVEL_ARRAY[i] - _lightLevelValue))
                colourTempValIndex = min(range(len(COLOUR_TEMPERATURE_ARRAY)),
                                         key=lambda i: abs(COLOUR_TEMPERATURE_ARRAY[i] - _colourTemperatureValue))
                serial_msg = '25' + str(device_id) + '0017' + str(DALI_LIGHT_LEVEL_HEX_ARRAY[lightValIndex]) + str(
                    COLOUR_TEMPERATURE_HEX_ARRAY[colourTempValIndex]) + LUMIAIRE_MODE + 'FF\n'
                # uncomment for debugging
                print("writing ", str(serial_msg).encode(), " to " + str(_serialDevice.port))
                ser.write(str(serial_msg).encode())
                time.sleep(0.005)
            except (ValueError, IOError, Exception) as ex:
                # uncomment for debugging
                # print("error in serial communication : " + str(ex))
                return None

