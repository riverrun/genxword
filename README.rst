========
genxword
========

.. image:: https://github.com/riverrun/genxword/raw/master/icons/genxword-gtk.png
  :alt: genxword logo
  :align: right

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
It will not work with earlier versions of Python. The command line version depends on Py2cairo (or Pycairo), 
which is already installed on most popular distros, to produce the image files.
The GUI version depends on Pygobject (also known as python-gobject or python-gi).

To install this program, run the following commands (the **install** script needs to be run as root or with sudo)::

    git clone git://github.com/riverrun/genxword.git
    cd genxword
    sudo ./install_genxword.sh

Alternatively, go to the **Tags** or **Downloads** tab, download the **tar.gz** version, 
and run the following commands (again, the **install** script needs to be run as root or with sudo)::

    tar xvzf riverrun-genxword-xxxx.tar.gz
    cd riverrun-genxword-xxxx
    sudo ./install_genxword.sh

Authors
=======

This program was originally written by Bryan Helmig and has since been developed by David Whitlock. 

Note about svg files
====================

For users of Libreoffice, you will need version 3.5 to display the svg files properly. 
Older versions do not work. The svg files are displayed correctly in Chromium and Firefox.
