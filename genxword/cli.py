# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2020 David Whitlock
#
# Genxword is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Genxword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with genxword.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import argparse
from .control import _, Genxword

usage_info = _("""The word list file contains the words and clues, or just words, that you want in your crossword.
For further information on how to format the word list file and about the other options, please consult the man page.
""")

def main():
    parser = argparse.ArgumentParser(description=_('Crossword generator.'), prog='genxword', epilog=usage_info)
    parser.add_argument('infile', help=_('Name of word list file.'))
    parser.add_argument('saveformat', help=_('Save files as A4 pdf (p), letter size pdf (l), png (n), svg(s) and/or '
                                             'ipuz(z).'))
    parser.add_argument('-a', '--auto', dest='auto', action='store_true', help=_('Automated (non-interactive) option.'))
    parser.add_argument('-m', '--mix', dest='mixmode', action='store_true', help=_('Create anagrams for the clues'))
    parser.add_argument('-n', '--number', dest='nwords', type=int, default=50, help=_('Number of words to be used.'))
    parser.add_argument('-o', '--output', dest='output', default='Gumby', help=_('Name of crossword.'))
    args = parser.parse_args()
    gen = Genxword(args.auto, args.mixmode)
    with open(args.infile) as infile:
        gen.wlist(infile, args.nwords)
    gen.grid_size()
    gen.gengrid(args.output, args.saveformat)
