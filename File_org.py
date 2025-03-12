import os
import shutil

def organize_files(directory):
    """Organize files in a directory based on extensions."""
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = file.split('.')[-1]
            ext_folder = os.path.join(directory, ext)
            os.makedirs(ext_folder, exist_ok=True)
            shutil.move(file_path, os.path.join(ext_folder, file))
            print(f"Moved {file} to {ext_folder}")
