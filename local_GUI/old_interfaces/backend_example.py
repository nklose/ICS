"""
Example script to call the backend from the folder.
"""

import sys
import os.path

# Get the absolute path to the current directory
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
# Get the directory above the current directory.
ROOT_DIR = os.path.dirname(CUR_DIR)

sys.path.append(ROOT_DIR)

# Can now import the backend, or even the midend.
# Tools such as pylint will complain, but running this script will work.
import backend.dual as dual

(out, par, used_deltas) = dual.core(None, None, 4, 0, False)
print out
print par
print used_deltas
