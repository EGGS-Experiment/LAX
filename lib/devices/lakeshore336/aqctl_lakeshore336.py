from serial import Serial, PARITY_ODD
from sipyco.pc_rpc import simple_server_loop, Client
import logging, argparse
#import sipyco.common_args as sca

logger = logging.getLogger(__name__)

class Lakeshore336(object):
    def __init__(self, device_name):
        self.ser = Serial(device_name, baudrate = 57600, bytesize = 7, parity = PARITY_ODD, timeout = 1.0)

    def identify(self):
        self.ser.write("*IDN?\n".encode())
        return self.ser.readline().decode()

    def get_temp(self, input='0'):
        """
        Returns the temperature of an input channel as a float in Kelvin
        Args:
            input (str): either 0, 'A', 'B', 'C', or 'D' (0 is all channels)
        """
        self.ser.write('KRDG? ' + str(output_channel) + TERMINATOR)
        resp = self.ser.read_until()
        resp = np.array(resp.split(','), dtype=float)
        print(resp)
        return resp

    def close(self):
        self.ser.close()

def get_argparser():
    parser = argparse.ArgumentParser(description = "ARTIQ controller for LakeShore Cryogenics 336 temperature controllers")
    parser.add_argument("-d",\
                        "--device",\
                        default = "COM32",\
                        help = "device's hardware address")

    #adds arguments for default port
    sca.simple_network_args(parser, 3259)
    #adds logging arguments
    sca.verbosity_args(parser)
    return parser

def main():
    #passes added arguments to proper place
    args = get_argparser().parse_args()
    sca.init_logger_from_args(args)
    dev = Lakeshore336(args.device)
    try:
        simple_server_loop({"Lakeshore336": dev}, sca.bind_address_from_args(args),
                           args.port)
    finally:
        dev.close()

if __name__ == "__main__":
    main()
