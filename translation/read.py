import os
import re

# Get the current directory
current_directory = os.getcwd()

# Construct the file path
file_path = os.path.join(current_directory, "Container_366_51_142_20_revTannuri.p3d")

# Create text files to store the extracted information
output_fileG_path = os.path.join(current_directory, "extracted_geo.txt")
output_filePX_path = os.path.join(current_directory, "extracted_posx.txt")
output_filePY_path = os.path.join(current_directory, "extracted_posy.txt")
output_filePZ_path = os.path.join(current_directory, "extracted_posz.txt")
output_fileVX_path = os.path.join(current_directory, "extracted_velx.txt")
output_fileVY_path = os.path.join(current_directory, "extracted_vely.txt")

# Open the output files in write mode
with open(output_fileG_path, "w") as output_fileG, \
        open(output_filePX_path, "w") as output_filePX, \
        open(output_filePY_path, "w") as output_filePY, \
        open(output_filePZ_path, "w") as output_filePZ, \
        open(output_fileVX_path, "w") as output_fileVX, \
        open(output_fileVY_path, "w") as output_fileVY:

    # Read the file
    with open(file_path, "r") as file:
        data = file.read()

    georef_info = re.search(r'GEOREF\s*=\s*{(.*?)}', data, re.DOTALL)
    if georef_info:
        output_fileG.write(georef_info.group(1) + "\n")

    shadow_current_position_x_info = re.search(r'SHADOW_CURRENT_POSITION_X\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_x_info:
        output_filePX.write(shadow_current_position_x_info.group(1) + "\n")

    shadow_current_position_y_info = re.search(r'SHADOW_CURRENT_POSITION_Y\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_y_info:
        output_filePY.write(shadow_current_position_y_info.group(1) + "\n")

    shadow_current_position_z_info = re.search(r'SHADOW_CURRENT_POSITION_Z\s*=\s*{(.*?)}', data, re.DOTALL)
    if shadow_current_position_z_info:
        output_filePZ.write(shadow_current_position_z_info.group(1) + "\n")

    # Find and write shadow current velocity X
    shadow_current_velocity_x_info = re.search(r'SHADOW_CURRENT_VELOCITY_X\s*=\s*{([^A-Za-z]*)}', data, re.DOTALL)
    if shadow_current_velocity_x_info:
        output_fileVX.write(shadow_current_velocity_x_info.group(1) + "\n")

    # Find and write shadow current velocity Y
    shadow_current_velocity_y_info = re.search(r'SHADOW_CURRENT_VELOCITY_Y\s*=\s*{([^A-Za-z]*)}', data, re.DOTALL)
    if shadow_current_velocity_y_info:
  
        y_velocity_data = shadow_current_velocity_y_info.group(1).strip('{}').strip()
        output_fileVY.write(y_velocity_data + "\n")
