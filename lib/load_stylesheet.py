import sys
import os

# Function to load and apply the stylesheet from a file
def loadStylesheet(path):
     # Determine if the application is running as a script or as a bundled executable
    if getattr(sys, 'frozen', False):  # Check if we're in a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Directory of the script

    # Construct the full path to the stylesheet file
    file_path = os.path.join(base_path, path)

    # Open and read the stylesheet
    with open(file_path, "r") as file:
        stylesheet = file.read()

    return stylesheet