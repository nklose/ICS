from cx_Freeze import setup, Executable
import os.path

IMAGE_FOLDER = "Images"

BACKEND = "backend"

ROOT_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
LOCAL_GUI_PATH = os.path.join(ROOT_PATH, "local_GUI")
IMAGE_PATH = os.path.join(ROOT_PATH, IMAGE_FOLDER)
MAIN_FILE = os.path.join(ROOT_PATH, "local_start.py")
EXE_FILE = "ICS"
ICON_FILE = os.path.join(ROOT_PATH, "icon.ico")
LOCAL_IMAGES = [os.path.join(IMAGE_PATH, "r.png"),
                os.path.join(IMAGE_PATH, "g.png"),
                os.path.join(IMAGE_PATH, "b.png"),
                os.path.join(IMAGE_PATH, "rgb.png")]
BIN_FOLDER = os.path.join(ROOT_PATH, "bin")


LIB_BACKEND = os.path.join(BACKEND, "libbackend.so")
LIB_BACKEND_PATH = os.path.join(ROOT_PATH, LIB_BACKEND)

INCLUDES = ["sip", "scipy.linalg.cblas", "scipy.linalg.fblas",
            "ctypes", "scipy.linalg.flapack", "scipy.linalg.clapack",
            "matplotlib", "matplotlib.backends.backend_tkagg"]

# Dependencies are automatically detected, but it might need fine tuning.
include_files = [(a, os.path.join(IMAGE_FOLDER, os.path.basename(a)))
                 for a in LOCAL_IMAGES]
include_in_shared_zip = [(LIB_BACKEND_PATH, LIB_BACKEND)]
build_exe_options = {"packages": ["backend", "midend", "local_GUI"],
                     "excludes": [], "include_files": include_files,
                     "build_exe": BIN_FOLDER, "icon": "icon.ico",
                     "includes": INCLUDES, "compressed": False,
                     "create_shared_zip": False,
                     "constants": "HACKITY_HACK_HACK=True"}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(name="ICS",
      version="1.0",
      description="Image Correlation Spectroscopy",
      options={"build_exe": build_exe_options},
      executables=[Executable("local_start.py", targetName=EXE_FILE,
                              base=base)])
