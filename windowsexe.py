""" Requires py2exe

Call in cmd.exe (NOT MINGW SHELL):

C:\Python27\python.exe windowsexe.py py2exe

or

Call in mingw shell:

/c/Python27/python windowsexe.py py2exe
"""
from distutils.core import setup
import py2exe
import os
import sys
import numpy

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOCAL_GUI_PATH = os.path.join(ROOT_PATH, "local_GUI")
MAIN_FILE = os.path.join(LOCAL_GUI_PATH, "start.py")
EXE_FILE = "ICS"
ICON_FILE = "icon.ico"
LOCAL_IMAGES = [os.path.join(LOCAL_GUI_PATH, "r.png"),
                os.path.join(LOCAL_GUI_PATH, "g.png"),
                os.path.join(LOCAL_GUI_PATH, "b.png"),
                os.path.join(LOCAL_GUI_PATH, "rgb.png")]

AUTHOR = "CMPUT 401 - Biomembranes Team"
VERSION = "1.0"
DESCRIPTION = "Image Correlation Spectroscopy"
NAME = "ICS"

PACKAGES = ["backend", "midend", "local_GUI"]
INCLUDES = ["sip"]
EXCLUDES = []
DLL_EXCLUDES = ["libiomp5md.dll", "MSVCP90.dll"]
DATA_FILES = [('', LOCAL_IMAGES)]

OPTIONS = {
    'py2exe': {
        "dist_dir": "bin",
        "packages": PACKAGES,
        "includes": INCLUDES,
        "excludes": EXCLUDES,
        "dll_excludes": DLL_EXCLUDES,
        'bundle_files': 3,  # 1 = .exe; 2 = .zip; 3 = separate
        'compressed': 2,
        'optimize': 2,
        'xref': False,
        'skip_archive': False,
        'ascii': False,
    }
}

WINDOWS = [{"dest_base": EXE_FILE, "script": MAIN_FILE,
            "icon_resources": [(1, ICON_FILE)]
            }]

mydata_files = [
    ('', ['README.txt', 'Labelmaker.bat'])
]

setup(
    windows=WINDOWS,
    author=AUTHOR,
    version=VERSION,
    description=DESCRIPTION,
    name=NAME,
    options=OPTIONS,
    data_files=DATA_FILES,
    zipfile=None  # Libs go into the .exe
)
