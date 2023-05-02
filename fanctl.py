#!/usr/bin/env python3

import configparser
import glob
import os
import sys
import time

config = configparser.ConfigParser()
config.read("/etc/fanctl.conf")

general = config["general"] if "general" in config else config["DEFAULT"]
temp = config["temp"] if "temp" in config else config["DEFAULT"]

PROBE_INTERVAL = general.getint("ProbeInterval", 5)
TEMP_FAN_OFF = temp.getint("TempFanOff", 40)
TEMP_FAN_MAX = temp.getint("TempFanMax", 60)

def SetFanSpeed(percentage: int):
    if (percentage < 0 or percentage > 100):
        print(f'Error: bad percentage {percentage}')
        return
    os.system(f'i2cset -y -f 6 0x18 0x8a {percentage}')

def GetTemp(file) -> float:
    file.seek(0)
    return float(file.read()) / 1000.0

# Define fan policy based on temperature readings, returns a speed percentage between 0 and 100.
def FanPolicy(temps) -> int:
    highest_temp = max(temps.values())
    speed = 100 * (highest_temp - TEMP_FAN_OFF) / (TEMP_FAN_MAX - TEMP_FAN_OFF)
    speed = max(0, min(int(speed), 100))
    return speed

def main() -> int:
    os.system(f'fan.sh low')
    probes = {}
    for path in glob.glob('/sys/class/thermal/thermal_zone*'):
        try:
            with open(path + '/type', 'r') as file:
                name = file.read().splitlines()[0]
                probes[name] = open(path + '/temp', 'r')
                print(f'Connected to {name} at {path}')
        except:
            print (f'Failed to connect to {path}')
    print(f'Polling every {PROBE_INTERVAL}s...')
    while (True):
        temps = {}
        for name, file in probes.items():
            temps[name] = GetTemp(file)
        target = FanPolicy(temps)
        SetFanSpeed(target)
        # print(f'{target}: {temps}')
        time.sleep(PROBE_INTERVAL)
    return 0

if __name__ == '__main__':
    sys.exit(main())
