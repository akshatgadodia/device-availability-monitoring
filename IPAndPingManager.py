import ipaddress
import time
from datetime import datetime

import ping3

import constants
from DeviceAvailabilityDataManager import DeviceAvailabilityDataManager
from DeviceDataManager import DeviceDataManager


class IPAndPingManager:
    def __init__(self):
        """
        Initialize the IPAndPingManager class.
        This constructor sets up the IPAndPingManager object and initializes the DeviceDataManager and
        DeviceAvailabilityDataManager objects to manage device data and availability data, respectively.
        """
        self.device_data_manager: DeviceDataManager = DeviceDataManager()
        self.device_availability_data_manager: DeviceAvailabilityDataManager = DeviceAvailabilityDataManager()

    def __str__(self):
        """
        Return a string representation of the IPAndPingManager object.

        Returns:
            str: A string representation of the IPAndPingManager object.
        """
        return "IPAndPingManager"

    def __repr__(self):
        """
        Return a string representation of the IPAndPingManager object.

        Returns:
            str: A string representation of the IPAndPingManager object.
        """
        return f"IPAndPingManager()"

    def ping_all_devices(self) -> None:
        """
        Pings all the devices and store the results, every 5 minutes
        Return:
            None
        """
        ping_cycle = 1
        interval: int = 300
        while True:
            start_time = time.time()
            devices_data: dict[str, dict] = self.device_data_manager.load_device_data_file()
            devices_status_data: list[list] = []
            for device_id in devices_data:
                device_data: dict = devices_data.get(device_id)
                status: int = IPAndPingManager.ping_device(device_data["ip"])
                devices_status_data.append([device_id, status, datetime.now()])
            self.device_availability_data_manager.save_device_availability_data_file(devices_status_data)
            end_time = time.time()
            execution_time = end_time - start_time
            remaining_time = interval - execution_time
            print(f"Ping Cycle {ping_cycle}: Ended at {datetime.now()}.\n"
                  f"Next ping cycle will start at {datetime.fromtimestamp(time.time() + remaining_time)}.")
            print("-" * 70)
            ping_cycle += 1
            if remaining_time > 0:
                time.sleep(remaining_time)

    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """
        Check if the ip is valid or not
        Args
            ip (str): IP to be validated
        Return:
            Bool: Return True if IP is valid otherwise False
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def ping_device(device_ip: str) -> int:
        """

        Args:
            device_ip (str): IP of the device to be pinged
        Returns:
            status (int): Status of the ping, 1 for success and 0 for failure
        """
        try:
            print(f"Pinging {device_ip}")
            ping = ping3.ping(device_ip)
            status = 1 if ping is not None and ping > 0 else 0
            print(f"{device_ip}: Active") if status else print(f"{device_ip}: Inactive")
            return status
        except OSError:
            print(constants.invalid_ip)
            status = 0
            return status
