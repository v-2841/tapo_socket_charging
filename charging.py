import ipaddress
import logging
import os
import subprocess
import sys
from time import sleep
from logging.handlers import RotatingFileHandler

import psutil
from dotenv import load_dotenv
from PyP100 import PyP100

from taskschd import add_to_taskschd, remove_from_taskschd


load_dotenv()
MAC_ADDRESS = os.getenv('MAC_ADDRESS').replace(':', '-')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
MIN_BATTERY_PERCENTAGE = 40
MAX_BATTERY_PERCENTAGE = 60
UPDATE_INTERVAL = 10
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[RotatingFileHandler(
        filename='main.log',
        maxBytes=1024 * 1024)],
)
logger = logging.getLogger(__name__)


def socket_init():
    global p100
    while True:
        try:
            socket_ip = subprocess.check_output(
                f'arp -a |findstr "{MAC_ADDRESS}"',
                shell=True).split()[0].decode('utf-8')
        except subprocess.CalledProcessError:
            logger.error('Socket MAC address not found. Retrying...')
            sleep(UPDATE_INTERVAL)
            continue
        try:
            socket_ip = ipaddress.ip_address(socket_ip)
        except ValueError:
            socket_ip = None
        if socket_ip:
            logger.info(f'Socket IP: {socket_ip}')
            try:
                p100 = PyP100.P100(socket_ip, EMAIL, PASSWORD)
                logger.info('Socket initialized.')
                break
            except Exception:
                logger.error('Failed to initialize socket. Retrying...')
                sleep(UPDATE_INTERVAL)
                continue
        logger.info('Socket IP not found. Retrying...')
        sleep(UPDATE_INTERVAL)


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--add-to-taskschd':
            add_to_taskschd()
            sys.exit(0)
        elif sys.argv[1] == '--remove-from-taskschd':
            remove_from_taskschd()
            sys.exit(0)
        else:
            print('Invalid argument.')
            sys.exit(1)
    socket_init()
    while True:
        battery = psutil.sensors_battery()
        logger.info(
            f'Battery: {battery.percent}%, charging: {battery.power_plugged}')
        if (battery.percent < MIN_BATTERY_PERCENTAGE
                and not battery.power_plugged):
            try:
                p100.turnOn()
                logger.info('Socket turned on.')
            except Exception:
                logger.error('Failed to turn on socket. Retrying...')
                socket_init()
        elif (battery.percent > MAX_BATTERY_PERCENTAGE
                and battery.power_plugged):
            try:
                p100.turnOff()
                logger.info('Socket turned off.')
            except Exception:
                logger.error('Failed to turn off socket. Retrying...')
                socket_init()
        sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    main()
