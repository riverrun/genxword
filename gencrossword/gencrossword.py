#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs an empty grid and key in png/svg format and a text file containing the words and clues.
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

usage_info = """Creates a crossword from a list of words and clues from a text file. You can save the crossword, with clues, as a 
pdf file, or you can save the empty grid and key in png and/or svg format, together with the word bank and clues in a text file.
You need to write the name of the text file you will use to create the word list. The text file can contain words and clues, or just single words.
If you are using a file with words and clues in it, each word should be separated from the clue by just a space, 
and each word and clue, or word, should be on a separate line.
The -n option lets you choose how many words will be randomly selected from the text file. The default is 50.
The -t option lets you change the maximum time taken to calculate the crossword. The default is 1 second.
Increasing this time will not make much difference, but the option is there if you want it.
"""

class Finishxword(object):
    def __init__(self, args):
        self.args = args

    def wlist(self):
        if self.args.nword:
            nword = self.args.nword
        else:
            nword = 50
        self.word_list = [line.strip().split(' ', 1) for line in self.args.infile]
        if len(self.word_list) > nword:
            self.word_list = random.sample(self.word_list, nword)

    def calctime(self):
        if self.args.time:
            self.tcalc = self.args.time
        else:
            self.tcalc = 1

    def grid_size(self):
        if len(self.word_list) <= 20:
            self.ncol = self.nrow = 17
        elif len(self.word_list) <= 100:
            self.ncol = self.nrow = int((round(((len(self.word_list) - 20) / 7.5), 0) * 2) + 19)
        else:
            self.ncol = self.nrow = 43
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
            a.compute_crossword(self.tcalc)
            print(a.solution())
            print(len(a.current_word_list), 'out of', len(self.word_list))
            h = raw_input('Are you happy with this solution? [Y/n] ')
            if h.strip() != 'n':
                break
            inc_gsize = raw_input('And increase the grid size? [Y/n] ')
            if inc_gsize.strip() != 'n':
                self.ncol += 2;self.nrow += 2
        a.create_files()

def main():
    parser = argparse.ArgumentParser(description='Crossword generator.', prog='genxword', epilog=usage_info)
    parser.add_argument('infile', type=argparse.FileType('r'), help='Name of file to be imported.')
    parser.add_argument('-n', '--number', dest='nword', type=int, help='Number of words to be used.')
    parser.add_argument('-t', '--time', dest='time', type=int, help='Time used to calculate the crossword.')
    args = parser.parse_args()
    g = Finishxword(args)
    g.wlist()
    g.calctime()
    g.grid_size()
    g.gengrid()

if __name__ == '__main__':
    main()
