========
genxword
========

---------------------
A crossword generator
---------------------

Description
===========

Creates a crossword from a list of words and clues from a text file. There is an option to save the crossword, with clues, as a 
pdf file, or you can save the empty grid and key in png and/or svg format, together with the word bank and clues in a text file.

Usage
=====

Genxword needs to be called with the name of the text file you will use to create the word list 
and the type of file that you want saved. The text file can contain words and clues, or just single words. 
If you are using a file with words and clues in it, each word should be separated from the clue by just a space, 
and each word and clue, or word, should be on a separate line. Some example word list files are in the **examples** directory.
The crossword can be saved as a pdf file, with clues, or as png/svg files, together with a text file 
containing the word bank and clues. All files are saved in the user's current working directory.

Example::

    genxword word_list.txt ps

This command will produce a crossword using words from the word_list.txt file and save the grid, with clues, 
as an A4-sized pdf file (p), the grid as an svg file (s), and a text file containing the word bank and clues.

The default grid size depends on how many words are used, but the user has the option to change this.
Once the crossword has been calculated, the user has the option to have it recalculated. 
Each time it is recalculated, the number of columns and the number of rows can both be increased. 

There are also options to specify the number of words used in the crossword and 
the amount of time used to calculate it. In addition, the program can be run non-interactively. 
For further information, please consult the man page.

Installation
============

Linux
-----

To run this program, you need to have **python2.7** or **python3** installed. It will not work with earlier versions of python. 
It depends on py2cairo (or pycairo), which is already installed on most popular distros, to produce the image files.

To install this program, run the following commands (replace *python* with *python2* if you are using Arch Linux)::

    git clone git://github.com/riverrun/genxword.git
    cd genxword
    sudo python setup.py install
    sudo cp genxword /usr/local/bin/
    sudo chmod 755 /usr/local/bin/genxword

For use with **python3**, run the *py3-version.sh* script after changing to the *genxword* directory, 
replace *python* with *python3* in the third command, and then run the last two commands.

Alternatively, for either version, you can download a tarball from the **Downloads** tab, unpack it, 
change to the *riverrun-genxword-somenumber* directory, and then run the last three commands.

To install the man page, run the following commands (replace genxword.6 with genxword-py3.6 for use with **python3**)::

    cd man
    gzip genxword.6
    sudo cp genxword.6.gz /usr/share/man/man6/

Authors
=======

This program was originally written by Bryan Helmig and has since been developed by David Whitlock. 

Note about svg files
====================

The svg files are displayed correctly in Chromium and Firefox, but not in Libreoffice 3.4.4.
