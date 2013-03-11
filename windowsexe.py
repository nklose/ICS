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
import numpy

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
MAIN_FILE = os.path.join(ROOT_PATH, os.path.join("backend", "example.py"))
EXE_FILE = "ICS"
ICON_FILE = "icon.ico"

print "Main is %s" % MAIN_FILE

AUTHOR = "CMPUT 401 - Biomembranes Team"
VERSION = "1.0"
DESCRIPTION = "Image Correlation Spectroscopy"
NAME = "ICS"

PACKAGES = []
INCLUDES = []
EXCLUDES = []
DLL_EXCLUDES = ["libiomp5md.dll"]
#["MSVCP90.dll", 'libiomp5md.dll', 
#						 'libifcoremd.dll', 'libmmd.dll',
#						 'svml_dispmd.dll', 'libifportMD.dll']

OPTIONS = {
	'py2exe': {
		"dist_dir": "bin",
		"packages": PACKAGES,
		"includes": INCLUDES,
		#"excludes": EXCLUDES,
		"dll_excludes": DLL_EXCLUDES
    }
}

WINDOWS = [{"dest_base": EXE_FILE, "script": MAIN_FILE,
			"icon_resources": [(1, ICON_FILE)]
		   }]

setup(
	windows = WINDOWS,
	author = AUTHOR,
	version = VERSION,
	description = DESCRIPTION,
	name = NAME,
	options = OPTIONS
)