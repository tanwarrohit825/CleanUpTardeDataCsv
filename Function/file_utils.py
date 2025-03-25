import easygui

def findpath(title):
    """ Opens a file dialog and returns the cleaned file path. """
    file_path = easygui.fileopenbox(title)

    if file_path:
        return file_path.replace('\\', '/')
    else:
        print("No file selected.")
        return None
