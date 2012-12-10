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

Ubuntu-based distros
-----

Open a terminal and run the following commands::

    sudo add-apt-repository ppa:riverrun/genxword
    sudo apt-get update

And then to install the Python 2.7 version::

    sudo apt-get install genxword

Or alternatively, to install the Python 3 version::

    sudo apt-get install genxword3

Other distros
-----

To install this program, go to the **Downloads** tab, download the latest stable version, currently genxword-0.5.0, 
or genxword3-0.5.0 (the Python 3 version), and run the following commands (on each line, replace genxword with 
genxword3 if using the Python 3 version)::

    tar xvzf genxword-0.5.0.tar.gz
    cd genxword-0.5.0
    sudo ./install_genxword.sh

Authors
=======

This program has been developed by David Whitlock, and it is based on a program originally written by Bryan Helmig. 

Note about svg files
====================

For users of Libreoffice, you will need version 3.5 to display the svg files properly. 
Older versions do not work. The svg files are displayed correctly in Chromium and Firefox.
