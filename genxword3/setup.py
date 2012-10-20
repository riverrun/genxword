#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2012 David Whitlock
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import os
from distutils.core import setup

setup(
    name = 'genxword3',
    version = '0.5.0',
    packages = ['genxword3'],
    scripts = ['bin/genxword3', 'bin/genxword3-gtk'],
    data_files = [
        ('share/applications', ['genxword3-gtk.desktop']),
        ('share/pixmaps', ['genxword3-gtk.png']),
        ('share/genxword3', ['help_page']),
        ('share/genxword3/word_lists', ['word_lists/2000ENwords', 'word_lists/pythonwords']),
        ],
    author = 'David Whitlock',
    author_email = 'alovedalongthe@gmail.com',
    url = 'https://github.com/riverrun/genxword',
    description = 'A crossword generator',
    license = 'GPLv3',
)
