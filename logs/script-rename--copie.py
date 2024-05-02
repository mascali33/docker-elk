#!/usr/bin/env python3

import os

def rename_files(directory, prefix):
    # Get a list of files in the directory
    files = os.listdir(directory)
    
    # Sort files to maintain any existing order
    files.sort()
    
    # Loop through the files and rename them
    for idx, filename in enumerate(files):
        # Create the new file name
        if os.path.splitext(filename)[1] == '.his':
            # If you need more than 999 logs files replace the 3 in the next lines by a 4 or more
            formatted_index = f"{idx+1:03}"
            new_name = f"{prefix}{formatted_index}.his"
        
            # Generate full file path
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_name)
        
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_name}'")

# Example usage:
# Update the folder path and prefix name accordingly
folder_path = 'path_to_your_folder'  # Change this to the path of your folder
file_prefix = 'name'  # Change this to your desired prefix
# first parameter is the directory of the files you want to rename,
# second parameter is the starting of the name of the file you want to rename
rename_files(".", "etelm-logs-")

