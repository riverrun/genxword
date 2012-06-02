========
genxword
========

---------------------
A crossword generator
---------------------

Description
===========

Genxword is a crossword generator written in Python. There are now two versions, `genxword-gtk <https://github.com/riverrun/genxword/wiki/genxword-gtk>`_, which has a graphical user interface, and genxword, which runs from the command line. 
Both versions create a crossword from a list of words and clues. You can save the crossword, with clues, as a pdf file, 
or you can save the empty grid and key in png and/or svg format, together with the word bank and clues in a text file.

Usage
=====

Please read the wiki for information about how to use genxword.

Installation
============

Linux
-----

To run this program, you need to have **Python 2.7** or **Python 3** installed. 
It will not work with earlier versions of Python. The command line version depends on py2cairo (or pycairo), 
which is already installed on most popular distros, to produce the image files.
The GUI version depends on pygobject (also known as python-gobject or python-gi).

To install this program, go to the **Downloads** tab, download the latest stable version, currently genxword-v0.4.4, 
or genxword3-v0.4.4 (the Python 3 version), and run the following commands (replace genxword with genxword3 if 
using the Python 3 version). The **install** script needs to be run as root or with sudo::

    tar xvzf genxword-0.4.4.tar.gz
    cd genxword-0.4.4
    sudo ./install_genxword.sh

Authors
=======

This program has been developed by David Whitlock, and it is based on a program originally written by Bryan Helmig. 

Note about svg files
====================

For users of Libreoffice, you will need version 3.5 to display the svg files properly. 
Older versions do not work. The svg files are displayed correctly in Chromium and Firefox.
