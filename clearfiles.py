import os
import shutil

"""
Explanation of the Code:

1. The script imports necessary modules: `os` for file and directory operations, 
   and `shutil` for high-level file operations, such as removing directories.
2. Defines a function `empty_folder` that takes a folder path as input and empties 
   the specified folder by deleting all its files and subdirectories.
3. Checks if the specified folder exists; if not, it prints an appropriate message.
4. Iterates over each item in the folder, determining whether it's a file or a directory.
5. Deletes files and symbolic links using `os.unlink()`.
6. Deletes directories and their contents using `shutil.rmtree()`.
7. Includes error handling to catch and print any exceptions that occur during deletion.
"""


def empty_folder(folder_path):
    """
    Empties the specified folder by removing all files and directories inside it.

    Parameters:
    folder_path (str): The path to the folder to be emptied.

    Returns:
    None
    """
    
    # Check if the specified folder exists
    if os.path.exists(folder_path):
        # Loop through all files and directories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)  # Get the full path of the file/directory
            try:
                # Check if it's a file or a symbolic link and remove it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file or link
                # Check if it's a directory and remove its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the entire directory and its contents
            except Exception as e:
                # Print an error message if unable to delete a file/directory
                print(f'Error deleting {file_path}. Reason: {e}')
    else:
        # Print a message if the folder does not exist
        print(f"The folder {folder_path} does not exist.")

# Example usage
folder_path = '/home/user7/deploy/processed_images'  # Specify the path of the folder to be emptied
empty_folder(folder_path)  # Call the function to empty the specified folder
