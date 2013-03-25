import local_GUI.start as start
import matplotlib
import os


if __name__ == "__main__":
    if os.name == "nt":
		matplotlib.use("wxagg")
    start.start()
