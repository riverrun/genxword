#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs an empty grid and key in png/svg format and a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011 David Whitlock
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.core import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return "File '{}'.format(fname) not found.\n"

setup(
    name = 'genxword',
    version = '0.1.5',
    packages = ['gencrossword'],
    author = 'David Whitlock Bryan Helmig',
    author_email = 'alovedalongthe@gmail.com',
    url = 'https://github.com/riverrun/genxword',
    description = 'A crossword generator',
    long_description = read('README.rst'),
    license = 'GPLv3',
)
