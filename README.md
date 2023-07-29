# Device Availability Monitoring Application

The Device Availability Monitoring Application is a Python-based tool designed to monitor the availability of devices on a local network. It provides the ability to track the status of multiple devices, ping them at regular intervals, and store the availability data in CSV format for analysis.

## Features

- Device Data Management: The application allows you to add, view, update, and delete devices for monitoring. Device data, including unique device IDs, names, and IP addresses, is stored in a JSON file.

- Ping Status Tracking: The application periodically pings the devices at 5-minute intervals. Successful pings record the device status as "1," while unsuccessful pings record it as "0."

- Availability Data Storage: The device availability data is stored in CSV format, containing device IDs, status (0 or 1), and timestamps. Data is appended to the CSV file with corresponding timestamps for each 5-minute cycle.

- Command-Line Interface (CLI): The application includes a CLI to interact with the monitoring functionalities. Users can add, view, update, and delete devices through CLI commands.

## Files and Usage

1. `DeviceDataManager.py`: Manages device data, including adding, viewing, updating, and deleting devices. Run `python DeviceDataManager.py` to access the CLI for device data management.

2. `DeviceAvailabilityDataManager.py`: Manages device availability data, including viewing and filtering availability data. Run `python DeviceAvailabilityDataManager.py` to access the CLI for availability data management.

3. `IPAndPingManager.py`: Handles pinging devices and storing their availability data. Run `python IPAndPingManager.py` to ping all devices continuously.

4. `__main__.py`: Provides a comprehensive CLI interface to interact with device data and availability data functionalities. Run `python __main__.py --help` to view available commands.

5. `constants.py`: Contains constant messages and filenames used throughout the application.

## Setup and Requirements

1. Python 3: The application requires Python 3.11.4 to run.

2. Dependencies: Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

## How to Use

1. To add a new device for monitoring, run:
   ```
   python __main__.py --add-device
   ```

2. To view the list of devices, run:
   ```
   python __main__.py --view-devices
   ```

3. To view the details of a specific device by its ID, run:
   ```
   python __main__.py --view-device <DEVICE_ID>
   ```
   Replace `DEVICE_ID` with the actual ID of the device.<br /></br>

4. To update a device's information by specifying its ID, run:
   ```
   python __main__.py --update-device <DEVICE_ID>
   ```
   Replace `DEVICE_ID` with the actual ID of the device.<br /></br>

5. To delete a device by specifying its ID, run:
   ```
   python __main__.py --delete-device <DEVICE_ID>
   ```
   Replace `DEVICE_ID` with the actual ID of the device.<br /></br>

6. To view all the device availability data, run:
   ```
   python __main__.py --view-device-availability-data
   ```
7. To search for availability data by parameter type and value, run:
   ```
   python __main__.py --view-filtered-device-availability-data <parameter> <value>
   ```
   Replace `parameter` with `date` or `id` and `value` with the specific date or device ID you want to search for.
   <br /></br>

8. To ping a specific device by its IP, run:
   ```
   python __main__.py --ping-device <DEVICE_IP>
   ```
   Replace `DEVICE_IP` with the actual IP address of the device.<br /></br>

9. To start monitoring all devices and continuously ping them, run:
   ```
   python __main__.py --ping-devices
   ```

## Authors

The Device Availability Monitoring Application was developed by Akshat Gadodia as a part of AurigaIT Associate Software Developer Training.
