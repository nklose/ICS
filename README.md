BioMembrane
===========

CMPUT 401 Project 5 "Simulation and analysis of images for studies of biological
membranes" for Dr Nils O. Petersen.

Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar
Qadri, and James Wang under the 401 IP License.

Installing in Windows
=====================
Run the vcredist_x86.exe and the provided setup.exe

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
A few items are required:

1. Install python 2.7.3 (64-bit) to C:\Python27 and python 2.7.3 (32-bit) to C:\Python27_32
   (To use different paths, edit the Makefile).
2. Install mingw (32-bit).
3. Install scipy, numpy, pythonmagic and pyqt for 32 bit and 64-bit. Use premade
4. Install the Visual Studio C++ Redistributable version here: http://www.microsoft.com/en-us/download/details.aspx?id=29
5. Launch the mingw 32-bit shell:
     a. To create the 32 bit version, call "make"
	 b. To create the 64 bit version, call "make DLL_64=1"