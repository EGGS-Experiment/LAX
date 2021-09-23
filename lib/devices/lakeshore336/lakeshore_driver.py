from serial import Serial, PARITY_ODD

class LakeShore336:
    def __init__(self, device_name):
        self.ser = Serial(device_name, baudrate = 57600, bytesize = 7, parity = PARITY_ODD, timeout = 1.0)

    def identify(self):
        self.ser.write("*IDN?\n".encode())
        return self.ser.readline().decode()

    def get_temp(self, input="A"):
        """ Returns the temperature of an input channel as a float in Kelvin
        : param input: either "A" or "B"
        """
        self.stream.write("KRDG? {}\n".format(input).encode())
        return float(self.stream.readline())

    def close(self):
        self.ser.close()
