# -*- coding: utf-8 -*-
# This comment is required if there are any non-ASCII characters in the script file.

import os

# get the folder path where the script is
scriptDir = os.path.dirname(os.path.realpath(__file__))

# close open project if necessary:
if projects.primary:
    projects.primary.close()

# Create a new project
project = projects.create("C:/tmp/Codesysproject.project", True)

# Add PLC
project.add("Main controller", 4096, "1006 120D", "6.3.0.12")

parent_device = projects.primary.find('Main controller', True)[0]

#Add modules to the kbus
if not(parent_device == None):
    kbus = parent_device.find('Kbus', True)[0]

if not(kbus == None):
    kbus.add("750-430", 32776, "8801_0750043000000000", "2.0.0.14")

    kbus.add("750-530", 32776, "8802_0750053000000000", "2.0.0.15")

# Add CAN bus interface and CANopen manager
parent_device.add("CANbus", 15, "WAGO_CANbus", "3.5.17.4")

CANbus = parent_device.find('CANbus', True)[0]

CANbus.add("CANopen Manager", 16, "WAGO_CANOPEN_MANAGER", "3.5.4.10")

CANopenManager = CANbus.find('CANopen Manager', True)[0]

# Add remote IO (750-348)
CANopenManager.add("RIO", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19")

# Add modules to RIO
RIO_1 = CANopenManager.find('RIO', True)[0]

RIO_1.add("_430", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19", "42")
RIO_1.add("_530", 18, "21_15C", "Revision=16#00000001, FileVersion=1.19", "126")

# Import IO mapping
inputPath = os.path.join(scriptDir, "RIO_mapping.csv")

RIO_1.import_io_mappings_from_csv(inputPath)

# Import application
pouNativeExportPath = os.path.join(scriptDir, "WAGO.export")

Application = parent_device.find('Application', True)[0]

Application.import_native(pouNativeExportPath)

# Save project
project.save()