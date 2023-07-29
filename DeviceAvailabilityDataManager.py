import csv
import constants
from datetime import datetime
import os


class DeviceAvailabilityDataManager:
    """
    Class responsible for managing device availability data.
    Attributes:
        device_availability_data_filename (str): The filename of the CSV file to store device availability data.
    Methods:
        __init__(self) -> None:
            Initialize DeviceAvailabilityDataManager with the device availability data filename.
        __str__(self) -> str:
            Return a string representation of the DeviceAvailabilityDataManager object.
        __repr__(self) -> str:
            Return a string representation that can be used to recreate the DeviceAvailabilityDataManager object.
        load_device_availability_data_file(self) -> list[list]:
            Load device availability data from the CSV file.
        print_all_device_availability_data(self) -> None:\
            Print all the device availability data in a tabular format.
        print_device_availability_data_by_parameter(self, parameter: str, value: str) -> None:
            Print device availability data filtered by parameter and value.
        save_device_availability_data_file(self, data: list[list]) -> None:
            Save device availability data to the CSV file.
        """
    def __init__(self):
        """
        Initialize DeviceAvailabilityDataManager with the device availability data filename.
        Returns:
            None
        """
        self.device_availability_data_filename = constants.device_data_availability_filename

    def __str__(self):
        """
        Return a string representation of the DeviceAvailabilityDataManager object.
        Returns:
            str: String representation of the object.
        """
        return "DeviceAvailabilityDataManager"

    def __repr__(self):
        """
        Return a string representation that can be used to recreate the DeviceAvailabilityDataManager object.
        Returns:
            str: String representation for recreation.
        """
        return "DeviceAvailabilityDataManager()"

    def load_device_availability_data_file(self) -> list[list]:
        """
        Load device availability data from the CSV file.
        Returns:
            list[list]: A list of lists containing device availability data, with each row representing a device's
                availability status and timestamp.
        Raises:
            FileNotFoundError: If the specified 'device_availability_data_filename' is not found, a new CSV file will be
                created with headers and returned.
        """
        try:
            with open(self.device_availability_data_filename) as file:
                reader = csv.reader(file)
                device_availability_data: list[list] = list(reader)
                return device_availability_data
        except FileNotFoundError:
            print("File Not Found")
            print(f"Creating File {self.device_availability_data_filename}")
            headers = ["Device Id", "Status", "Timestamp"]
            with open(self.device_availability_data_filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
            return [headers]

    def print_all_device_availability_data(self) -> None:
        """
        Print all the device availability data in a tabular format.
        Returns:
            None
        """
        device_availability_data: list = self.load_device_availability_data_file()
        if len(device_availability_data) == 1:
            print(constants.no_device_availability_data_found)
            return
        row_template = "{:^15} {:^10} {:^40}"
        print(row_template.format(device_availability_data[0][0],
                                  device_availability_data[0][1],
                                  device_availability_data[0][2]))
        for availability_data in device_availability_data[1::]:
            print(row_template.format(availability_data[0], availability_data[1], availability_data[2]))

    def print_device_availability_data_by_parameter(self, parameter: str, value: str) -> None:
        """
        Print device availability data filtered by parameter and value.
        Args:
            parameter (str): The parameter by which to filter the device availability data.
            value (str): The value to filter the device availability data for the specified parameter.
        Returns:
            None
        """
        device_availability_data: list = self.load_device_availability_data_file()
        if len(device_availability_data) == 1:
            print(constants.no_device_availability_data_found)
            return
        row_template = "{:^15} {:^10} {:^40}"
        print(row_template.format(device_availability_data[0][0],
                                  device_availability_data[0][1],
                                  device_availability_data[0][2]))
        if parameter == "date":
            try:
                target_date = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use 'YYYY-MM-DD' format.")
                return
            for row in device_availability_data[1:]:
                timestamp = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f").date()
                if timestamp == target_date:
                    print(row_template.format(row[0], row[1], row[2]))
        elif parameter == "id":
            for row in device_availability_data[1:]:
                if row[0] == value:
                    print(row_template.format(row[0], row[1], row[2]))
        else:
            print("Invalid parameter. Please use 'date' or 'id' as the parameter.")

    def save_device_availability_data_file(self, data: list[list]) -> None:
        """
        Save device availability data to the CSV file.
        Args:
            data (list[list]): The list of lists containing device availability data to be saved.
        Returns:
            None
        """
        file_exists = os.path.isfile(self.device_availability_data_filename)
        with open(self.device_availability_data_filename, "a", newline="") as file:
            writer_object = csv.writer(file, lineterminator='\n')
            if not file_exists:
                headers = ["Device Id", "Status", "Timestamp"]
                writer_object.writerow(headers)
            writer_object.writerows(data)
