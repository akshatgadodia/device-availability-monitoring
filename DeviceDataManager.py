import json
import constants


class DeviceDataManager:
    """
    Class responsible for managing device data.
    Attributes:
        device_data_filename (str): The filename of the JSON file to store device data.
    Methods:
        __init__(self) -> None:
            Initialize DeviceDataManager with the device data filename.
        __str__() -> str:
            Return a string representation of the DeviceDataManager object.
        __repr__() -> str:
            Return a string representation that can be used to recreate the DeviceDataManager object.
        load_device_data_file() -> dict[str, dict]:
            Load device data from the JSON file.
        check_if_id_exists(device_id: str) -> bool:
            Check if a device ID exists in the device data.
        add_device(device_id: str, device_name: str, device_ip: str) -> None:
            Add a new device to the device data.
        print_all_device_data() -> None:
            Print all the device data in a tabular format.
        print_device_data_by_id(device_id: str) -> None:
            Print device data for a specific device ID.
        get_device_data_by_id(device_id: str) -> dict | None:
            Get device data for a specific device ID.
        update_device_data_by_id(device_id: str, device_name: str, device_ip: str) -> None:
            Update device data for a specific device ID.
        delete_device_by_id(device_id: str) -> None:
            Delete a device from the device data by its ID.
        save_device_data_file(data: dict[str, dict]) -> None:
            Save device data to the JSON file.
    """

    def __init__(self):
        """
        Initialize DeviceDataManager with the device data filename.
        """
        self.device_data_filename = constants.device_data_filename

    def __str__(self):
        """
        Return a string representation of the DeviceDataManager object.
        Returns:
            str: String representation of the object.
        """
        return f"DeviceDataManager with device_data_filename: {self.device_data_filename}"

    def __repr__(self):
        """
        Return a string representation that can be used to recreate the DeviceDataManager object.
        Returns:
            str: String representation for recreation.
        """
        return f"DeviceDataManager()"

    def load_device_data_file(self) -> dict[str, dict] | dict:
        """
        Load or get the device data from the device data file.
        Returns:
            dict[str, dict]: A dictionary containing device data with device IDs as keys and
            device information (name and IP address) as nested dictionaries.
        Raises:
            FileNotFoundError: If the specified 'device_data_filename' is not found, a new
                JSON file will be created with an empty dictionary and returned.
            json.JSONDecodeError: If the JSON file is empty or contains invalid JSON data,
                a new JSON file will be created with an empty dictionary and returned.
        """
        try:
            with open(self.device_data_filename) as file:
                return json.load(file)
        except FileNotFoundError:
            print("File Not Found")
            print(f"Creating File {self.device_data_filename}")
            with open(self.device_data_filename, "w") as file:
                json.dump({}, file)
        except json.JSONDecodeError:
            print("Empty JSON File")
            with open(self.device_data_filename, "w") as file:
                json.dump({}, file)
            return {}

    def check_if_id_exists(self, device_id: str) -> bool:
        """
        Check if a device ID exists in the loaded device data.
        Args:
            device_id (str): The unique identifier of the device to be checked.
        Returns:
            bool: True if the 'device_id' exists in the loaded device data, False otherwise.
        """
        devices_data: dict[str, dict] = self.load_device_data_file()
        return device_id in devices_data

    def add_device(self, device_id: str, device_name: str, device_ip: str) -> None:
        """
        Add a new device to the device data.
        Args:
            device_id (str): The unique identifier for the new device.
            device_name (str): The name of the new device.
            device_ip (str): The IP address of the new device.
        Return:
            None
        """
        if self.check_if_id_exists(device_id):
            print(constants.device_with_id_already_exists)
            return
        if device_name == "" or device_ip == "":
            print(constants.device_name_ip_not_provided)
            return
        devices_data: dict[str, dict] = self.load_device_data_file()
        devices_data[device_id] = {'name': device_name, 'ip': device_ip}
        self.save_device_data_file(devices_data)
        print(constants.device_added_successfully)

    def print_all_device_data(self) -> None:
        """
        Print all the device data present in devices data file
        Return:
           None
        """
        devices_data: dict[str, dict] = self.load_device_data_file()
        row_template = "{:^15} {:^20} {:^20}"
        print(row_template.format("Device Id", "Device Name", "Device IP"))
        for device_id in devices_data:
            print(row_template.format(device_id, devices_data[device_id]['name'], devices_data[device_id]['ip']))

    def print_device_data_by_id(self, device_id: str) -> None:
        """
        Prints the device details by id
        Args:
            device_id (str): The unique identifier of the device to be printed.
        Return:
           None
        """
        if not self.check_if_id_exists(device_id):
            print(constants.device_not_found_message)
            return
        devices_data: dict[str, dict] = self.load_device_data_file()
        row_template = "{:^15} {:^20} {:^20}"
        print(row_template.format("Device Id", "Device Name", "Device IP"))
        print(row_template.format(device_id, devices_data[device_id]['name'], devices_data[device_id]['ip']))

    def get_device_data_by_id(self, device_id: str) -> dict | None:
        """
        Get the details of a specific device using its ID.
        Args:
            device_id (str): The unique identifier of the device to be retrieved.
        Returns:
            dict or None: A dictionary containing the device details with 'name' and 'ip' keys,
                            or None if the device ID does not exist in the device data.
        """
        if not self.check_if_id_exists(device_id):
            print(constants.device_not_found_message)
            return
        devices_data: dict[str, dict] = self.load_device_data_file()
        return devices_data.get(device_id)

    def update_device_data_by_id(self, device_id: str, device_name: str,
                                 device_ip: str) -> None:
        """
        Update the details of a specific device using its ID.
        Args:
            device_id (str): The unique identifier of the device to be updated.
            device_name (str): The new name of the device.
            device_ip (str): The new IP address of the device.
        Returns:
            None
        """
        if not self.check_if_id_exists(device_id):
            print(constants.device_not_found_message)
            return
        devices_data: dict[str, dict] = self.load_device_data_file()
        if device_name != "":
            devices_data[device_id]["name"] = device_name
        if device_ip != "":
            devices_data[device_id]["ip"] = device_ip
        self.save_device_data_file(devices_data)
        print(constants.device_updated_successfully)

    def delete_device_by_id(self, device_id: str) -> None:
        """
        Delete the device from device data file
        Args:
            device_id (str): The unique identifier of the device to be deleted.
        Returns:
            None
        """
        if not self.check_if_id_exists(device_id):
            print(constants.device_not_found_message)
            return
        devices_data: dict[str, dict] = self.load_device_data_file()
        devices_data.pop(device_id)
        self.save_device_data_file(devices_data)
        print(constants.device_deleted_successfully)

    def save_device_data_file(self, data: dict[str, dict]) -> None:
        """
        Save the device data in device data file
        Args:
            data (dict[str, dict]): The dictionary containing the device data to be saved.
        Returns:
            None
        """
        with open(self.device_data_filename, "w") as file:
            file_data = json.dumps(data, indent=4)
            file.write(file_data)
