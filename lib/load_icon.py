import os
import sys
from PyQt5.QtGui import QIcon

def loadIcon(path):
     # Determine if the application is running as a script or as a bundled executable
    if getattr(sys, 'frozen', False):  # Check if we're in a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary folder used by PyInstaller
    else:
        base_path = os.path.dirname(__file__)  # Directory of the script

    # Construct the full path to the icon
    file_path = os.path.join(base_path, path)

    return QIcon(file_path)