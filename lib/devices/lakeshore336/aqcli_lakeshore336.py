#!/usr/bin/env python3

from sipyco.pc_rpc import Client
import sipyco.common_args as sca

def main():
    remote = Client("::1", 3259, "Lakeshore336")
    try:
        remote.get_temp('A')
    finally:
        remote.close_rpc()

if __name__ == "__main__":
    main()