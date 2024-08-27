import os
import subprocess
import re
from pathlib import Path

from fire_helmet.exceptions import CameraException


def camera_reset():
    try:
        print(os.getcwd())
        p = Path("fire_helmet/usb/usbreset").resolve()
        bus_rx = r"Bus (\d+)"
        device_rx = r"Device (\d+)"

        result = subprocess.run("lsusb | grep 3D", shell=True, capture_output=True, text=True, check=True).stdout
        bus = re.findall(bus_rx, result)[0]
        device = re.findall(device_rx, result)[0]

        device_path = f"/dev/bus/usb/{bus}/{device}"
        subprocess.run(["sudo", p, device_path], check=True)

    except subprocess.CalledProcessError as e:
        raise CameraException
