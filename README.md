# CODESYS Project Automation with Python

## Overview
This Python script automates the creation and configuration of a CODESYS project using the WAGO PLC system. The script performs the following actions:

1. **Initialize the environment**: Determines the script's directory and closes any open projects.
2. **Create a new project**: Saves it to a predefined location.
3. **Add a main PLC controller**: Configures it with specific parameters.
4. **Attach modules to the Kbus**: Adds I/O modules to the controller.
5. **Configure the CANbus interface**: Includes a CANopen manager and remote I/O.
6. **Import I/O mappings**: Loads mappings from a CSV file.
7. **Import application logic**: Loads preconfigured logic from an export file.
8. **Save the project**.

## Script Breakdown

### 1. Import Required Libraries
```python
import os
```
This script utilizes the `os` module to handle file paths dynamically.

### 2. Define the Script Directory
```python
scriptDir = os.path.dirname(os.path.realpath(__file__))
```
This ensures all file operations reference the script's location.

### 3. Close Any Open Project
```python
if projects.primary:
    projects.primary.close()
```
This prevents conflicts by closing any currently open CODESYS projects.

### 4. Create a New Project
```python
project = projects.create("C:/tmp/Codesysproject.project", True)
```
A new project file is created at the specified path.

### 5. Add the Main PLC Controller
```python
project.add("Main controller", 4096, "1006 120D", "6.3.1.1")
```
Defines a WAGO PLC as the primary controller.

### 6. Add Modules to the Kbus
```python
parent_device = projects.primary.find('Main controller', True)[0]
```
Finds the main controller as a parent device.

```python
if not(parent_device == None):
    kbus = parent_device.find('Kbus', True)[0]
```
Retrieves the Kbus interface for module integration.

```python
if not(kbus == None):
    kbus.add("750-430", 32776, "8801_0750043000000000", "2.0.0.14")
    kbus.add("750-530", 32776, "8802_0750053000000000", "2.0.0.15")
```
Two I/O modules are added to the Kbus.

### 7. Configure CANbus and CANopen Manager
```python
parent_device.add("CANbus", 15, "WAGO_CANbus", "3.5.17.4")
CANbus = parent_device.find('CANbus', True)[0]
CANbus.add("CANopen Manager", 16, "WAGO_CANOPEN_MANAGER", "3.5.4.10")
CANopenManager = CANbus.find('CANopen Manager', True)[0]
```
A CANbus interface and a CANopen manager are configured.

### 8. Add Remote I/O and Modules
```python
CANopenManager.add("RIO", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19")
RIO_1 = CANopenManager.find('RIO', True)[0]
RIO_1.add("_430", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19", "42")
RIO_1.add("_530", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19", "126")
```
Remote I/O and additional modules are integrated into the system.

### 9. Import I/O Mappings
```python
inputPath = os.path.join(scriptDir, "RIO_mapping.csv")
RIO_1.import_io_mappings_from_csv(inputPath)
```
I/O mappings are imported from a CSV file.

### 10. Import Application Logic
```python
pouNativeExportPath = os.path.join(scriptDir, "WAGO.export")
Application = parent_device.find('Application', True)[0]
Application.import_native(pouNativeExportPath)
```
The application logic is imported from an external file.

### 11. Save the Project
```python
project.save()
```
Saves the configured CODESYS project.

## Conclusion
This Python script provides an automated way to set up a CODESYS project with WAGO PLCs, including I/O modules, CANbus interfaces, and application logic. By using this approach, engineers can streamline the configuration process and ensure consistency across multiple deployments.
