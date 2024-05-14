import os
import re

# Get the current directory
current_directory = os.getcwd()

# Construct the file path
file_path = os.path.join(current_directory, "Container_366_51_142_20_revTannuri.p3d")

# Create a text file to store the extracted information
output_file_path = os.path.join(current_directory, "extracted_info.txt")

# Open the output file in write mode
with open(output_file_path, "w") as output_file:

    # Read the file
    with open(file_path, "r") as file:
        data = file.read()
    
    georef_info = re.search(r'GEOREF\s*=\s*{(.*?)}', data, re.DOTALL)
    if georef_info:
        output_file.write("Georef Info:\n")
        output_file.write(georef_info.group(1) + "\n")

    shadow_current_position_x_info = re.search(r'SHADOW_CURRENT_POSITION_X\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_x_info:
        output_file.write("SHADOW_CURRENT_POSITION_X:\n")
        output_file.write(shadow_current_position_x_info.group(1) + "\n")

    shadow_current_position_y_info = re.search(r'SHADOW_CURRENT_POSITION_Y\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_y_info:
        output_file.write("SHADOW_CURRENT_POSITION_Y:\n")
        output_file.write(shadow_current_position_y_info.group(1) + "\n")
        
    shadow_current_position_z_info = re.search(r'SHADOW_CURRENT_POSITION_Z\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_z_info:
        output_file.write("SHADOW_CURRENT_POSITION_Z:\n")
        output_file.write(shadow_current_position_z_info.group(1) + "\n")
        
    # Find and write shadow current velocity X
    shadow_current_velocity_x_info = re.search(r'SHADOW_CURRENT_VELOCITY_X\s*=\s*{([^A-Za-z]*)}', data, re.DOTALL)
    if shadow_current_velocity_x_info:
        output_file.write("SHADOW_CURRENT_VELOCITY_X:\n")
        output_file.write(shadow_current_velocity_x_info.group(1) + "\n")
    
    # Find and write shadow current velocity Y
    shadow_current_velocity_y_info = re.search(r'SHADOW_CURRENT_VELOCITY_Y\s*=\s*{([^A-Za-z]*)}', data, re.DOTALL)
    if shadow_current_velocity_y_info:
        output_file.write("SHADOW_CURRENT_VELOCITY_Y:\n")
        output_file.write(shadow_current_velocity_y_info.group(1) + "\n")