import os
import easygui

def findpath(title):
    """ Opens a file dialog in a specific directory and returns the cleaned file path. """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go one level up and then into the Csv folder
    target_folder = os.path.join(script_dir, '..', 'Csv')
    target_folder = os.path.abspath(target_folder)  # Normalize path

    # Build default path for easygui
    default_path = os.path.join(target_folder, '*')  # * means show all files

    # Open file dialog starting in the target folder
    file_path = easygui.fileopenbox(title, default=default_path)

    if file_path:
        return file_path.replace('\\', '/')
    else:
        print("No file selected.")
        return None
