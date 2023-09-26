import os
import sys
import click
import time
import logging
import re
import serial
import subprocess
import signal
from datetime import datetime as dt

from nordicsemi.dfu.bl_dfu_sett import BLDFUSettings
from nordicsemi.dfu.dfu import Dfu
from nordicsemi.dfu.dfu_transport import DfuEvent, TRANSPORT_LOGGING_LEVEL
from nordicsemi.dfu.dfu_transport_serial import DfuTransportSerial
from nordicsemi.dfu.package import Package
from nordicsemi import version as nrfutil_version
from nordicsemi.dfu.signing import Signing
from nordicsemi.zigbee.prod_config import ProductionConfig, ProductionConfigWrongException, ProductionConfigTooLargeException
from pc_ble_driver_py.exceptions import NordicSemiException
from nordicsemi.lister.device_lister import DeviceLister
import spinel.util as util

logger = logging.getLogger(__name__)

global_bar = None
def update_progress(progress=0):
    if global_bar:
        global_bar.update(progress)

def do_serial(package, port, connect_delay, flow_control, packet_receipt_notification, baud_rate, serial_number, ping,
              timeout):

    if flow_control is None:
        flow_control = DfuTransportSerial.DEFAULT_FLOW_CONTROL
    if packet_receipt_notification is None:
        packet_receipt_notification = DfuTransportSerial.DEFAULT_PRN
    if baud_rate is None:
        baud_rate = DfuTransportSerial.DEFAULT_BAUD_RATE
    if ping is None:
        ping = False
    if port is None:
        device_lister = DeviceLister()
        device = device_lister.get_device(serial_number=serial_number)
        if device is None:
            raise NordicSemiException("A device with serial number %s is not connected." % serial_number)
        port = device.get_first_available_com_port()
        logger.info("Resolved serial number {} to port {}".format(serial_number, port))

    if timeout is None:
        timeout = DfuTransportSerial.DEFAULT_TIMEOUT

    logger.info("Using board at serial port: {}".format(port))
    serial_backend = DfuTransportSerial(com_port=str(port), baud_rate=baud_rate,
                                        flow_control=flow_control, prn=packet_receipt_notification, do_ping=ping,
                                        timeout=timeout)
    serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, update_progress)
    dfu = Dfu(zip_file_path = package, dfu_transport = serial_backend, connect_delay = connect_delay)

    if logger.getEffectiveLevel() > logging.INFO:
        with click.progressbar(length=dfu.dfu_get_total_size()) as bar:
            global global_bar
            global_bar = bar
            dfu.dfu_send_images()
    else:
        dfu.dfu_send_images()

    click.echo("Device programmed.")

def usb_serial(package, port, connect_delay, flow_control, packet_receipt_notification, baud_rate, serial_number,
               timeout):
    """Perform a Device Firmware Update on a device with a bootloader that supports USB serial DFU."""
    do_serial(package, port, connect_delay, flow_control, packet_receipt_notification, baud_rate, serial_number, False,
              timeout)

# Stop greengrass so that we can access the serial port
os.system("sudo systemctl stop greengrass") 

# open the dongle serial port
ser = serial.Serial('/dev/ttyACM0')  

# Send the bootloader command
ser.write(b'AT ENTERBL\r\n')

#  Close the port
ser.close()

# Get the firmware file path
zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Folium_Dongle-2-6-2-OTA-Image.zip')

# Nordic library handles the rest
try:
    usb_serial(zip_file_path, '/dev/ttyACM0', None, None, None, None, None, None)
except():
    print("Failed to update the dongle firmware.")
    print("Restarting Greengrass.")

# TODO if the update fails can the dongle be stuck in BL mode?

# Run greengrass again.
os.system("sudo systemctl start greengrass") 