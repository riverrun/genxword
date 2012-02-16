#!/usr/bin/python2.7
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse, random
from . import calcxword

usage_info = """The word list file contains the words and clues, or just words, that you want in your crossword. 
For further information on how to format the word list file and about the other options, please consult the man page.
"""

class Finishxword(object):
    def __init__(self, args):
        self.args = args

    def wlist(self):
        self.word_list = [line.strip().split(' ', 1) for line in self.args.infile if line.strip()]
        if len(self.word_list) > self.args.nword:
            self.word_list = random.sample(self.word_list, self.args.nword)

    def grid_size(self):
        if len(self.word_list) <= 20:
            self.ncol = self.nrow = 17
        elif len(self.word_list) <= 100:
            self.ncol = self.nrow = int((round(((len(self.word_list) - 20) / 7.5), 0) * 2) + 19)
        else:
            self.ncol = self.nrow = 43
        if not self.args.auto:
            gsize = str(self.ncol) + ', ' + str(self.nrow)
            grid_size = raw_input('Enter grid size (' + gsize + ' is the default): ')
            if grid_size:
                try:
                    self.ncol, self.nrow = int(grid_size.split(',')[0]), int(grid_size.split(',')[1])
                except:
                    pass

    def gengrid(self):
        while 1:
            a = calcxword.Crossword(self.ncol, self.nrow, '-', self.word_list)
            print('Calculating your crossword...')
            a.compute_crossword(self.args.time)
            print(a.solution())
            print(len(a.current_word_list), 'out of', len(self.word_list))
            if self.args.auto:
                if float(len(a.current_word_list))/len(self.word_list) < 0.9:
                    self.ncol += 2;self.nrow += 2
                else:
                    break
            else:
                h = raw_input('Are you happy with this solution? [Y/n] ')
                if h.strip() != 'n':
                    break
                inc_gsize = raw_input('And increase the grid size? [Y/n] ')
                if inc_gsize.strip() != 'n':
                    self.ncol += 2;self.nrow += 2
        name = self.args.output
        if not self.args.auto and name == 'Gumby':
            name = raw_input('Enter a name for your crossword: ')
        a.create_files(name, self.args.saveopts)

def main():
    parser = argparse.ArgumentParser(description='Crossword generator.', prog='genxword', epilog=usage_info)
    parser.add_argument('infile', type=argparse.FileType('r'), help='Name of word list file. Required argument.')
    parser.add_argument('saveopts', help='Save as A4 pdf (p), letter-size pdf (l), png (n) and/or svg (s).')
    parser.add_argument('-a', '--auto', dest='auto', action='store_true', help='Automated (non-interactive) option.')
    parser.add_argument('-n', '--number', dest='nword', type=int, default=50, help='Number of words to be used.')
    parser.add_argument('-o', '--output', dest='output', default='Gumby', help='Name of crossword.')
    parser.add_argument('-t', '--time', dest='time', type=int, default=1, help='Time used to calculate the crossword.')
    args = parser.parse_args()
    g = Finishxword(args)
    g.wlist()
    g.grid_size()
    g.gengrid()

if __name__ == '__main__':
    main()
