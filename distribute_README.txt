=======================================================
======== Image Correlation Spectroscopy (ICS) =========
=======================================================
Copryight (c) 2013 Nick Klose, Richard Leung, Cameron Mann, Glen Nelson, Omar Qadri, and James Wang

Beta V2.1

NOTE: This application is currently in BETA.

Changes since Beta V1
=====================
- All correlations now works!
- Res Norm is now Displayed
- Graphs are now generated
- Triple Correlations are computed
- Separate images are being combined and displayed
- The Progress bar has been temporarily disabled.
- Fixed: The speed is temporarily slightly slower. This is due to an optimization step that needs to be worked around.
- Separate channels appear Red / Green / Blue, rather then grayscale.
- Fixed: Error log messages appear after trying to load an image that has been previously loaded.
- Fixed: Canceling an image selection may cause the program to cease responding.
- Fixed: Some of our systems experience crashes when the user attempts to load a monochrome image.
- Fixed: Permission error 13 on startup.
- Fixed: Log messages after running the program


Installation
============
1. Run the provided setup.exe, and complete the steps listed.
2. When the Microsoft Visual C++ 2008 Redistributable setup starts, install it as well.
3. Run the Image Correlation Spectroscopy from the start menu.

Working Features
================
1. Auto and Cross correlations calculate and display all output.
2. RGB and monochrome images can be loaded, and are displayed in the interface.
3. RGB images, when loaded, are split into each of the three channels. Each channel is previewed in grayscale.
4. The interface provides file checking to ensure images have the correct number of channels and are stored in a compatible format.
5. The interface provides input checking to ensure at least one channel (for autocorrelation) or channel pair (for cross-correlation) has been selected, that no parameters are missing, and that all parameters are numeric.
6. The start button and progress bar are functional. The interface disables the start button when correlation is in place, and jumps to the appropriate output tab.
7. The triple-correlation process.
8. All correlations works.

Known Bugs/Issues
=================
1. Export button has not been added.
2. Batch mode has not yet been implemented.
3. The stop button is not fully functional.
4. The Progress bar has been temporarily disabled.