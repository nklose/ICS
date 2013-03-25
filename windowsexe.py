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
import scipy
import matplotlib

IMAGE_FOLDER = "Images"

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOCAL_GUI_PATH = os.path.join(ROOT_PATH, "local_GUI")
IMAGE_PATH = os.path.join(ROOT_PATH, IMAGE_FOLDER)
MAIN_FILE = os.path.join(ROOT_PATH, "local_start.py")
EXE_FILE = "ICS"
ICON_FILE = os.path.join(ROOT_PATH, "icon.ico")
LOCAL_IMAGES = [os.path.join(IMAGE_PATH, "r.png"),
                os.path.join(IMAGE_PATH, "g.png"),
                os.path.join(IMAGE_PATH, "b.png"),
                os.path.join(IMAGE_PATH, "rgb.png")]

AUTHOR = "CMPUT 401 - Biomembranes Team"
VERSION = "1.0"
DESCRIPTION = "Image Correlation Spectroscopy"
NAME = "ICS"

PACKAGES = ["backend", "midend", "local_GUI"]
INCLUDES = ["sip", "scipy.linalg.cblas", "scipy.linalg.fblas",
            "scipy.sparse.csgraph._validation", "ctypes",
            "scipy.linalg.flapack", "scipy.linalg.clapack", "matplotlib",
			"matplotlib.backends.backend_tkagg"]
EXCLUDES = ["_gtkagg", "_tkagg"]
DLL_EXCLUDES = ["libiomp5md.dll", "MSVCP90.dll", "numpy.linalg.lapack_lite.pyd",
                "libgdk-win32-2.0-0.dll", 'libgobject-2.0-0.dll']

QT_ICON_DLL = r'C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'
DATA_FILES = [(IMAGE_FOLDER, LOCAL_IMAGES), ("", [ICON_FILE]),
			  ('imageformats', [QT_ICON_DLL])]
DATA_FILES.extend(matplotlib.get_py2exe_datafiles())

OPTIONS = {
    'py2exe': {
        "dist_dir": "bin",
        "packages": PACKAGES,
        "includes": INCLUDES,
        "excludes": EXCLUDES,
        "dll_excludes": DLL_EXCLUDES,
        'bundle_files': 3,  # 1 = .exe; 2 = .zip; 3 = separate
        'compressed': 2,
        'optimize': 0,  # Must be disabled for matplotlib. Fixable with edits, see http://www.py2exe.org/index.cgi/MatPlotLib
        'xref': False,
        'skip_archive': False,
        'ascii': False,
    }
}

# Icon works only in windows xp
WINDOWS = [{"dest_base": EXE_FILE, "script": MAIN_FILE,
            "icon_resources": [(0, ICON_FILE)]
            }]

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
