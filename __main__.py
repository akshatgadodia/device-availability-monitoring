import argparse
from DeviceDataManager import DeviceDataManager
from DeviceAvailabilityDataManager import DeviceAvailabilityDataManager
from IPAndPingManager import IPAndPingManager


def setup_args_parser():
    """
    Set up the argument parser for the command-line interface.
    Returns:
        argparse.ArgumentParser: Argument parser with defined command-line options.
    """
    args_parsers = argparse.ArgumentParser(
        prog="Device Availability Monitoring",
        description="This program monitors the availability of devices on a local network."
    )
    args_parsers.add_argument(
        "--add-device",
        action="store_true",
        help="Add a new device for monitoring"
    )
    args_parsers.add_argument(
        "--view-devices",
        action="store_true",
        help="View the list of devices"
    )
    args_parsers.add_argument(
        "--view-device",
        # action="store" default
        type=str,
        help="View the list of devices"
    )
    args_parsers.add_argument(
        "--update-device",
        type=str,
        help="Update a device's information by specifying its ID"
    )
    args_parsers.add_argument(
        "--delete-device",
        type=str,
        help="Delete a device by specifying its ID"
    )
    args_parsers.add_argument(
        "--view-device-availability-data",
        action="store_true",
        help="View all the device availability data."
    )
    args_parsers.add_argument(
        "--view-filtered-device-availability-data",
        nargs=2,
        metavar=("<parameter_type>", "<value>"),
        help="Search for availability data by parameter type and value. Example: --device-availability-data date " +
             "<date>, --device-availability-data id <device-id>"
    )
    args_parsers.add_argument(
        "--ping-devices",
        action="store_true",
        help="Start monitoring the devices"
    )
    args_parsers.add_argument(
        "--ping-device",
        type=str,
        help="Ping a device by its ip"
    )
    return args_parsers


def get_valid_input(prompt: str, validation_func: callable, not_empty=True, error_message=None):
    """
    Get valid user input by prompting the user and validating it.
    Args:
        prompt (str): The prompt message for the user.
        validation_func (callable): A validation function to check the user input.
        not_empty (bool, optional): Set to False if empty input is allowed. Defaults to True.
        error_message (str, optional): Print custom error message when provided
    Returns:
        any: The validated user input.
    """
    while True:
        user_input: any = input(prompt).strip()
        condition: bool = user_input != "" and validation_func(user_input) if not_empty else validation_func(user_input)
        if condition:
            return user_input
        print(error_message) if error_message is not None else print("Invalid input. Please try again.")


def main() -> None:
    """
    Main function to execute the Device Availability Monitoring program.
    Returns:
        None
    """
    device_data_manager: DeviceDataManager = DeviceDataManager()
    device_availability_data_manager: DeviceAvailabilityDataManager = DeviceAvailabilityDataManager()
    ip_and_ping_manager: IPAndPingManager = IPAndPingManager()
    args_parsers = setup_args_parser()
    argument = args_parsers.parse_args()
    if argument.add_device:
        device_id: str = get_valid_input("Enter Device ID (No Spaces Allowed): ",
                                         lambda deviceid: not device_data_manager.check_if_id_exists(deviceid)
                                         and " " not in deviceid, error_message="Device ID already exists or contains "
                                         "spaces. Please enter a unique Device ID.")
        device_name: str = get_valid_input("Enter Device Name: ", lambda name: name != "")
        device_ip: str = get_valid_input("Enter Device IP: ", ip_and_ping_manager.is_valid_ip)
        device_data_manager.add_device(device_id, device_name.strip(), device_ip)
    elif argument.view_devices:
        device_data_manager.print_all_device_data()
    elif argument.view_device:
        device_id: str = argument.view_device
        if not device_data_manager.check_if_id_exists(device_id):
            print("Invalid Device Id")
            device_id: str = get_valid_input("Enter Device ID: ", device_data_manager.check_if_id_exists)
        device_data_manager.print_device_data_by_id(device_id)
    elif argument.update_device:
        device_id: str = argument.update_device
        if not device_data_manager.check_if_id_exists(device_id):
            print("Invalid Device Id")
            device_id: str = get_valid_input("Enter Device ID: ", device_data_manager.check_if_id_exists)
        device_data: dict = device_data_manager.get_device_data_by_id(device_id)

        print(f"Enter Device Name (Current is : {device_data['name']})")
        device_name: str = input("(Leave Blank for same): ")
        print(f"Enter Device IP: (Current is: {device_data['ip']})")
        device_ip: str = get_valid_input("(Leave Blank for same): ",
                                         lambda user_device_ip: True if user_device_ip == ""
                                         else ip_and_ping_manager.is_valid_ip(user_device_ip), not_empty=False)
        device_data_manager.update_device_data_by_id(device_id, device_name, device_ip)
    elif argument.delete_device:
        device_id: str = argument.delete_device
        if not device_data_manager.check_if_id_exists(device_id):
            print("Invalid Device Id")
            device_id: str = get_valid_input("Enter Device ID: ", device_data_manager.check_if_id_exists)
        device_data_manager.print_device_data_by_id(device_id)
        confirmation = input("Are you sure you want to delete this device? (y/n): ")
        while True:
            match confirmation:
                case 'y':
                    device_data_manager.delete_device_by_id(device_id)
                    return
                case 'n':
                    return
                case _:
                    confirmation = input("Please enter valid operation (y/n): ")
    elif argument.view_device_availability_data:
        device_availability_data_manager.print_all_device_availability_data()
    elif argument.view_filtered_device_availability_data:
        parameter, value = argument.view_filtered_device_availability_data
        if parameter == "id" and not device_data_manager.check_if_id_exists(value):
            print("Invalid Id")
            return
        device_availability_data_manager.print_device_availability_data_by_parameter(parameter, value)
    elif argument.ping_device:
        device_ip: str = argument.ping_device
        if not ip_and_ping_manager.is_valid_ip(device_ip):
            print("Invalid IP")
            device_ip: str = get_valid_input("Enter Device IP: ", ip_and_ping_manager.is_valid_ip)
        ip_and_ping_manager.ping_device(device_ip)
    elif argument.ping_devices:
        ip_and_ping_manager.ping_all_devices()
    else:
        args_parsers.print_help()


main()
