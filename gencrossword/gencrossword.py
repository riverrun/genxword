#!/usr/bin/python2
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

import argparse, random, calcxword

usage_info = """Creates a crossword from a list of words and clues typed on the command line
or from a text file. Outputs an empty grid and key in png and/or svg format, and the word bank and clues in a text file.
The -i option lets you use a text file to create the word list. The text file can contain words and clues, or just single words.
If you are using a file with words and clues in it, each word should be separated from the clue by just a space, 
and each word and clue, or word, should be on a separate line.
The -n option lets you choose how many words will be randomly selected from the text file. The default is 50.
The -t option lets you change the time taken to calculate the crossword. The default is 2 seconds.
You might need to increase this time if you are creating a large crossword, but it will only really help 
if you increase the grid size as well.
"""

class Finishxword(object):
    def __init__(self):
        self.word_list = []

    def wlist(self):
        if args.inputfile:
            if args.nword:
                nword = args.nword
            else:
                nword = 50
            self.word_list = [line.strip().split(' ', 1) for line in args.inputfile]
            self.word_list = random.sample(self.word_list, nword)
        else:
            self.word_list = []
            print('Enter the words and clues for your crossword below.\n\
When you have finished writing your words and clues, just press enter to start calculating the crossword.')
            wcount = 1
            while 1:
                x = raw_input('Enter word number ' + str(wcount) + ': ')
                if x == '':
                    break
                y = raw_input('Enter clue number ' + str(wcount) + ': ')
                self.word_list.append([x, y])
                wcount += 1

    def calctime(self):
        if args.time:
            self.tcalc = args.time
        else:
            self.tcalc = 2

    def grid_size(self):
        if len(self.word_list) <= 20:
            self.ncol, self.nrow = 17, 17
        elif len(self.word_list) <= 30:
            self.ncol, self.nrow = 19, 19
        elif len(self.word_list) <= 40:
            self.ncol, self.nrow = 21, 21
        else:
            self.ncol, self.nrow = 23, 23
        gsize = str(self.ncol) + ', ' + str(self.nrow)
        grid_size = raw_input('Enter grid size (' + gsize + ' is the default): ')
        if grid_size:
            try:
                self.ncol, self.nrow = int(grid_size.split(',')[0]), int(grid_size.split(',')[1])
            except:
                pass

    def gengrid(self):
        a = calcxword.Crossword(self.ncol, self.nrow, '-', 5000, self.word_list)
        while 1:
            print('Calculating your crossword...')
            a.compute_crossword(self.tcalc)
            print(a.solution())
            print(len(a.current_word_list), 'out of', len(self.word_list))
            print(a.debug)
            h = raw_input('Are you happy with this solution? [Y/n] ')
            if h != 'n':
                break
        xword_name = raw_input('Enter a name for your crossword: ')
        img_type = raw_input('Do you want to save the empty grid and key as png files, svg or both? [P/s/b] ')
        if img_type == 'b':
            a.img_grid(xword_name + '_grid.png')
            a.img_grid(xword_name + '_key.png')
            a.img_grid(xword_name + '_grid.svg')
            a.img_grid(xword_name + '_key.svg')
            print('The files ' + xword_name + '_grid.png, ' + xword_name + '_key.png, '
                    + xword_name + '_grid.svg, ' + xword_name + '_key.svg and ' 
                    + xword_name + '_clues.txt\nhave been saved to your current working directory.')
        elif img_type == 's':
            a.img_grid(xword_name + '_grid.svg')
            a.img_grid(xword_name + '_key.svg')
            print('The files ' + xword_name + '_grid.svg, ' + xword_name + '_key.svg and ' 
                    + xword_name + '_clues.txt\nhave been saved to your current working directory.')
        else:
            a.img_grid(xword_name + '_grid.png')
            a.img_grid(xword_name + '_key.png')
            print('The files ' + xword_name + '_grid.png, ' + xword_name + '_key.png and ' 
                    + xword_name + '_clues.txt\nhave been saved to your current working directory.')
        a.clues_txt(xword_name + '_clues.txt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crossword generator.', prog='genxword', epilog=usage_info)
    parser.add_argument('-i', '--inputfile', type=argparse.FileType('r'), dest='inputfile', help='Name of file to be imported.')
    parser.add_argument('-n', '--number', dest='nword', type=int, help='Number of words to be used.')
    parser.add_argument('-t', '--time', dest='time', type=int, help='Time used to calculate the crossword.')
    args = parser.parse_args()
    g = Finishxword()
    g.wlist()
    g.calctime()
    g.grid_size()
    g.gengrid()
