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
It will not work with earlier versions of Python.

Ubuntu-based distros
--------------------

Open a terminal and run the following commands::

    sudo add-apt-repository ppa:riverrun/genxword
    sudo apt-get update

And then to install the Python 2.7 version::

    sudo apt-get install genxword

Or alternatively, to install the Python 3 version::

    sudo apt-get install genxword3

Archlinux
---------

There are PKGBUILDs available at `genxword-git <https://aur.archlinux.org/packages.php?ID=53985>`_
and `genxword3-git <https://aur.archlinux.org/packages.php?ID=58514>`_.

Other distros
-------------

Go to the **Tags** tab, near the top of this page, download the latest stable version, 
currently genxword-0.5.0, extract the files, and run the following commands.

For the Python 2.7 version::

    cd genxword-0.5.0/genxword
    sudo ./install_genxword.sh

And for the Python 3 version::

    cd genxword-0.5.0/genxword3
    sudo ./install_genxword3.sh

The GUI version depends on pycairo (python-cairo), pygobject (python-gobject or python-gi) 
and gtksourceview3 (gir1.2-gtksource-3.0).
The command line version just depends on pycairo.

Authors
=======

This program has been developed by David Whitlock, and it is based on a program originally written by Bryan Helmig. 

Note about svg files
====================

For users of Libreoffice, you will need version 3.5 to display the svg files properly. 
Older versions do not work. The svg files are displayed correctly in Chromium and Firefox.
