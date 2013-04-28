# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2013 David Whitlock
#
# Genxword3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Genxword3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with genxword3.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import random
from . import calculate

usage_info = """The word list file contains the words and clues, or just words, that you want in your crossword. 
For further information on how to format the word list file and about the other options, please consult the man page.
"""

class Genxword(object):
    def __init__(self, auto=False):
        self.auto = auto

    def wlist(self, infile, nwords=50):
        word_list = [line.strip().split(' ', 1) for line in infile if line.strip()]
        if len(word_list) > nwords:
            word_list = random.sample(word_list, nwords)
        self.word_list = [[word[0].upper(), word[-1]] for word in word_list]
        self.word_list.sort(key=lambda i: len(i[0]), reverse=True)

    def grid_size(self, gtkmode=False):
        if len(self.word_list) <= 20:
            self.nrow = self.ncol = 17
        elif len(self.word_list) <= 100:
            self.nrow = self.ncol = int((round((len(self.word_list) - 20) / 8) * 2) + 19)
        else:
            self.nrow = self.ncol = 41
        if not gtkmode and not self.auto:
            gsize = str(self.nrow) + ', ' + str(self.ncol)
            grid_size = input('Enter grid size (' + gsize + ' is the default): ')
            if grid_size:
                self.check_grid_size(grid_size)

    def check_grid_size(self, grid_size):
        try:
            nrow, ncol = int(grid_size.split(',')[0]), int(grid_size.split(',')[1])
        except:
            pass
        else:
            if len(self.word_list[0][0]) < min(nrow, ncol):
                self.nrow, self.ncol = nrow, ncol

    def gengrid(self, name, saveformat, RTL):
        while 1:
            print('Calculating your crossword...')
            calc = calculate.Crossword(self.nrow, self.ncol, ' ', self.word_list)
            print(calc.compute_crossword(RTL, False))
            if self.auto:
                if len(calc.best_word_list)/len(self.word_list) < 0.9:
                    self.nrow += 2;self.ncol += 2
                else:
                    break
            else:
                h = input('Are you happy with this solution? [Y/n] ')
                if h.strip() != 'n':
                    break
                inc_gsize = input('And increase the grid size? [Y/n] ')
                if inc_gsize.strip() != 'n':
                    self.nrow += 2;self.ncol += 2
        exp = calculate.Exportfiles(self.nrow, self.ncol, calc.best_grid, calc.best_word_list)
        exp.create_files(name, saveformat, RTL)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Crossword generator.', prog='genxword3', epilog=usage_info)
    parser.add_argument('infile', type=argparse.FileType('r'), help='Name of word list file.')
    parser.add_argument('saveformat', help='Save files as A4 pdf (p), letter size pdf (l), png (n) and/or svg (s).')
    parser.add_argument('-a', '--auto', dest='auto', action='store_true', help='Automated (non-interactive) option.')
    parser.add_argument('-n', '--number', dest='nwords', type=int, default=50, help='Number of words to be used.')
    parser.add_argument('-r', '--rtl', dest='rtl', action='store_true', help='Right-to-left text.')
    parser.add_argument('-o', '--output', dest='output', default='Gumby', help='Name of crossword.')
    args = parser.parse_args()
    gen = Genxword(args.auto)
    gen.wlist(args.infile, args.nwords)
    gen.grid_size()
    gen.gengrid(args.output, args.saveformat, args.rtl)
