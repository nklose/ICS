=======================================================
======== Image Correlation Spectroscopy (ICS) =========
=======================================================
Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar Qadri, and James Wang

NOTE: This application is currently in BETA.

Installation
============
1. Run the provided setup.exe, and complete the steps listed.
2. When the Microsoft Visual C++ 2008 Redistributable setup starts, install it as well.
3. Run the Image Correlation Spectroscopy from the start menu.

Working Features
================
1. Auto and Cross correlations calculate and display all output values with the exception of Res. Norm.
2. RGB and monochrome images can be loaded, and are displayed in the interface.
3. RGB images, when loaded, are split into each of the three channels. Each channel is previewed in grayscale.
4. The interface provides file checking to ensure images have the correct number of channels and are stored in a compatible format.
5. The interface provides input checking to ensure at least one channel (for autocorrelation) or channel pair (for cross-correlation) has been selected, that no parameters are missing, and that all parameters are numeric.
6. The start button and progress bar are functional. The interface disables the start button when correlation is in place, and jumps to the appropriate output tab.
7. The triple-correlation process of enabling/disabling certain GUI elements and reading input is working, though the actual correlation is not yet calculated.

Known Bugs/Issues
=================
1. Res Norm is not displayed on the results.
2. Graphs are not generated.
3. Triple correlations are not yet computed.
4. Export button has not been added.
5. Batch mode has not yet been implemented.
6. Separate images are not being combined and displayed.
7. Separate channels do not appear colored Red / Green / Blue, but rather grayscale.
8. Error log messages appear after trying to load an image that has been previously loaded.
9. Canceling an image selection may cause the program to cease responding.
10. Some of our systems experience crashes when the user attempts to load a monochrome image.
11. The stop button is not fully functional.