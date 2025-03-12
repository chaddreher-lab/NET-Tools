#test
import os
import shutil

def remove_file(file_path):
    """Remove a file if it exists."""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' removed successfully.")
        else:
            print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error removing file '{file_path}': {e}")

def remove_folder(folder_path):
    """Remove a folder and its contents if it exists."""
    try:
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' removed successfully.")
        else:
            print(f"Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"Error removing folder '{folder_path}': {e}")

if __name__ == "__main__":
    while True:
        print("\nFile and Folder Removal Options:")
        print("1. Remove a file")
        print("2. Remove a folder")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            file_path = input("Enter the full path of the file to remove: ")
            remove_file(file_path)
        elif choice == "2":
            folder_path = input("Enter the full path of the folder to remove: ")
            remove_folder(folder_path)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")