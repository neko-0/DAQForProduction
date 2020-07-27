"""
class to retrive humidity and temperature from the sensor inside the chamber
"""

import serial

class TempSensor:
    def __init__(self):
        self.com = '/dev/ttyACM0'
        self.ser = serial.Serial(self.com, 9600)

    def getData(self):
        temp = self.ser.readline().decode('utf-8')
        humid = self.ser.readline().decode('utf-8')

        # At least catches temp/humidity mismatch when below 0C
        if float(humid) < 0:
            xtemp = humid
            humid = temp
            temp = xtemp

        odata = {
            "humidity": float(humid),
            "temperature": float(temp),
        }
        return odata

    def get_temperature(self):
        data = self.getData()
        return float(data["temperature"])

    def get_humidity(self):
        data = self.getData()
        return float(data["humidity"])

if __name__ == "__main__":

    """
    Test
    """
    Sensor = TempSensor()
    Data = Sensor.getData()
    print("Temperature:", Data["temperature"])
    print("Humidity:", Data["humidity"])