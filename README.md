BioMembrane
===========

CMPUT 401 Project 5 "Simulation and analysis of images for studies of biological
membranes" for Dr Nils O. Petersen.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

Required Packages
=================
A few packages are required for the program:

1. scipy. scipy is Copyright (c) 2005-2013, SciPy Developers and is licensed
   under the BSD License.
2. numpy. numpy is Copyright (c) 2005-2013, NumPy Developers and is licensed
   under the BSD License.
3. django. django is Copyright (c) 2005-2013, Django Software Foundation and
   is licensed under the BSD License.
4. fftw3. FFTW is Copyright (c) 2003, 2007-11 Matteo Frigo,
   Copyright (c) 2003, 2007-11 Massachusetts Institute of Technology
   and is licensed under the GPL (version 2 or later) License.
5. pythonmagick (Ubuntu package: python-pythonmagick). pythonmagick Copyright
1999-2011 ImageMagick Studio LLC, a non-profit organization dedicated to making
software imaging solutions freely available.

6. PyQT. PyQT is Copyright (c) 2013, Riverbank Computing Limited.
   Riverbank Computing Limited is a company registered in England and Wales
   with company number 4314904.

In addition, if you wish to run testcases, the following modules are required:

1. mock (sudo pip install -U mock). mock is Copyright (c) 2003-2010, Michael
   Foord and is licensed under the BSD License.


Compiling Windows Executables
=============================
Windows 64 bit executables turned out to be too difficult to support.
A few items are required:

1. Install python 2.7.3 (32-bit) to C:\Python27 (To use different paths,
   edit the Makefile).
2. Install mingw (32-bit).
3. Install required libraries:
     a. scipy, numpy, pythonmagick, matplotlib, and pil (use pillow) for
        32-bit. Use premade packages available at:
        http://www.lfd.uci.edu/~gohlke/pythonlibs/
	 b. py2exe: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/
	 c. pyqt: http://www.riverbankcomputing.com/software/pyqt/download
	    Version 4.10 has been successfully used.
4. Install the Visual Studio C++ Redistributable version here:
   http://www.microsoft.com/en-us/download/details.aspx?id=29 (included in repo)
5. Launch the mingw 32-bit shell:
     a. To create the 32 bit version, call "make"
     b. (DOESN'T WORK) To create the 64 bit version, call "make DLL_64=1"
6. To make the icon work, install pywin32:
   http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/

Compliing Linux Executables
===========================
1. Install cx-freeze:

    sudo apt-get install cx-freeze

2. edit `/usr/lib/pymodules/python2.7/cx_Freeze/finder.py`, on line 232 change

    path = parentModule.path

to

    path = parentModule.path or parentModule.file

3. Find the mpl-data directory (for me was in `/usr/share/matplotlib/mpl-data`)
4. Make a link to it in `/usr/lib/pymodules/python2.7/matplotlib/mpl-data`

    sudo ln -s /usr/share/matplotlib/mpl-data /usr/lib/pymodules/python2.7/matplotlib/mpl-data

5. Fix the broken font links, if any, in mpl-data/fonts/ttf (in my case,
   `cmex10.ttf`, `cmmi10.ttf`, `cmr10.ttf`, and `cmsy10.ttf` were broken, had to
    point them to my LyX installation)
6. Run the makefile
7. Distribute bin