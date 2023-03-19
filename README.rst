genxword
========

A crossword generator
---------------------

Description
-----------

Genxword is a crossword generator written in Python.

When you install genxword, you will have two programs,
`genxword-gtk <https://github.com/riverrun/genxword/wiki/genxword-gtk>`_,
which has a graphical user interface, and genxword, which runs from the
command line.

Both programs create a crossword from a list of words and
clues. You can save the crossword, with clues, as a pdf file, or you can
save the empty grid and key in png and/or svg format, together with the
word bank and clues in a text file.

Features
--------

-  The crossword can be saved, with clues, as a pdf file, or the empty
   grid and key can be saved in png and/or svg format, together with the
   word bank and clues in a text file.
-  The crossword can be recalculated multiple times - with the option to
   increase the grid size at each stage.
-  A dictionary file can be used as the word list. A certain amount of
   words (default 50) will be randomly selected from the file and used
   to make the crossword.
-  When editing the word list, there is an option to sort it, from the
   shortest to the longest word, and remove non-alphabetic characters.
-  Multiple languages, including right-to-left languages, such as Hebrew
   and Arabic, are now supported.

Use
---

Please read the `wiki <https://github.com/riverrun/genxword/wiki>`_ for
information about how to use genxword.

GUI Installation
----------------

To install genxword (add *sudo* to the command, or run as root,
if you are using Linux):

    pip3 install genxword

Next, ensure you have installed all the necessary dependencies under #Dependencies.

Lite Installation
-----------------

Simply run:

   pip3 install genxword --no-deps

Everything will work fine. However, you will only be able to export to:
   t: Text,
   z: IPUZ,
   c: CSV,
   j: Simplified JSON Representation

Dependencies
------------

Genxword requires pycairo (python-cairo), pygobject (python-gobject or python-gi),
python-gi-cairo (if you are using a Debian-based system), and pango (gir1.2-pango-1.0).

If you would like to use the GUI, install gtksourceview3 (gir1.2-gtksource-3.0) and gettext.

These dependencies can easily be installed on Linux by using your package manager,
and with most distributions, they will already be installed.

Windows users can download these dependencies from 
`here <http://sourceforge.net/projects/pygobjectwin32/files/?source=navbar>`_
When installing python-gobject, you also need to install (check the boxes for)
gtk3, pango, gdk-pixbuf and gtksourceview3.

Authors
-------

This program has been developed by David Whitlock, and it is based on a
program originally written by Bryan Helmig.

Translators
-----------

Many thanks to the following people, who have kindly provided translations for genxword:

Miguel Anxo Bouzada (Catalan, Spanish and Galician), Koen Wybo (Dutch), Pinkvana Thaworn (Thai)
and me (French).
