========
genxword
========

---------------------
A crossword generator
---------------------

Description
===========

Creates a crossword from a list of words and clues typed on the command line 
or from a text file. Outputs an empty grid and key in png and/or svg format, 
and the word bank and clues in a text file.

History
=======

This program was originally written by Bryan Helmig and has since been developed by David Whitlock 
although the business end of the program, the crossword algorithm, has largely been left intact (if it ain't broken, don't fix it!).

Usage
=====

If genxword is called without any options, the user is invited to enter the words and clues for the crossword. 
At this stage, the clues can be left empty. After writing all the words, the user just needs to press enter, 
instead of entering a word, to start calculating the crossword.

The default grid size depends on how many words are used, but the user has the option to change this.

Once the crossword has been calculated, the user has the option to have it recalculated. 
Each time it is recalculated, the number of columns and the number of rows can both be increased. 
Finally, the user decides what format to save the image files in, and then these files 
and a text file is saved in the user's current working directory.

Using a text file
-----------------

The -i option lets you use a text file to create the word list. The text file can contain words and clues, or just single words. 
If you are using a file with words and clues in it, each word should be separated from the clue by just a space, 
and each word and clue, or word, should be on a separate line.

The -n option lets you choose how many words will be randomly selected from the text file. The default is 50.

Example::

    genxword -i word_list.txt -n 40

This command will produce a crossword using 40 words randomly selected from the word_list.txt file, which can be several thousand words long.

Calculation time
----------------

The -t option lets you change the time taken to calculate the crossword. The default is 2 seconds. 
You might need to increase this time if you are creating a large crossword, but it will only really help 
if you increase the grid size as well.

Installation
============

This program has been tested with python2.7. It depends on py2cairo, which is already installed on most popular distros, to produce the image files.

To install this program, run the following commands (replace **python** with **python2** if you are using archlinux)::

    git clone git://github.com/riverrun/genxword.git
    cd genxword
    sudo python setup.py install
    sudo cp genxword /usr/local/bin/
    sudo chmod 755 /usr/local/bin/genxword

Instead of using the **git clone** command, you could also download the tarball from the **Downloads** tab,
unpack it and change to the *riverrun-genxword* directory, and then run the last three commands.

Note about svg files
====================

The svg files are displayed correctly in chromium and firefox, but not in Libreoffice 3.4.3.
