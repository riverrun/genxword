========
genxword
========

---------------------
A crossword generator
---------------------

Description
===========

Creates a crossword from a list of words and clues from a text file. There is an option to save the 
crossword, with clues, as a pdf file, or you can save the empty grid and key in png and/or svg format, 
together with the word bank and clues in a text file.

Usage
=====

Please read the wiki for information about how to use genxword.

Installation
============

Linux
-----

To run this program, you need to have **Python 2.7** or **Python 3** installed. 
It will not work with earlier versions of Python. It depends on Py2cairo (or Pycairo), 
which is already installed on most popular distros, to produce the image files.

To install this program, run the following commands (the **install** script needs to be run as root or with sudo)::

    git clone git://github.com/riverrun/genxword.git
    cd genxword
    ./install_genxword.sh

Alternatively, you can download a tarball from the **Tags** or **Downloads** tab, unpack it, 
change to the *riverrun-genxword-somenumber* directory, and then run the **install** script.

Authors
=======

This program was originally written by Bryan Helmig and has since been developed by David Whitlock. 

Note about svg files
====================

For users of Libreoffice, you will need version 3.5 to display the svg files properly. 
Older versions do not work. The svg files are displayed correctly in Chromium and Firefox.
