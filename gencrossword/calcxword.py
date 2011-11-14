# -*- coding: utf-8 -*-

"""Calculate the crossword and export image and text files."""

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

import random, re, time, string, cairo
from copy import copy as duplicate
 
class Crossword(object):
    def __init__(self, cols, rows, empty = '-', maxloops = 2000, available_words=[]):
        self.cols = cols
        self.rows = rows
        self.empty = empty
        self.maxloops = maxloops
        self.available_words = available_words
        self.current_word_list = []
        self.prep_grid_words()
 
    def prep_grid_words(self):
        """Initialize grid and word list."""
        self.grid = [[self.empty for j in range(self.cols)] for i in range(self.rows)]
        try:
            temp_list = [Word(word.word, word.clue) if isinstance(word, Word) else Word(word[0], word[1]) for word in self.available_words]
        except:
            temp_list = [Word(word[0], 'Write clue for ' + word[0]) for word in self.available_words]
        random.shuffle(temp_list) # randomize word list
        temp_list.sort(key=lambda i: len(i.word), reverse=True) # sort by length
        self.available_words = temp_list
 
    def compute_crossword(self, time_permitted = 1.00, spins=2):
        time_permitted = float(time_permitted)
 
        count = 0
        copy = Crossword(self.cols, self.rows, self.empty, self.maxloops, self.available_words)
 
        start_full = float(time.time())
        while (float(time.time()) - start_full) < time_permitted or count == 0:
            copy.current_word_list = []
            copy.prep_grid_words()
            x = 0
            while x < spins: # spins; 2 seems to be plenty
                for word in copy.available_words:
                    if word not in copy.current_word_list:
                        copy.fit_and_add(word)
                x += 1
            # buffer the best crossword by comparing placed words
            if len(copy.current_word_list) > len(self.current_word_list):
                self.current_word_list = copy.current_word_list
                self.grid = copy.grid
            if len(self.current_word_list) == len(self.available_words):
                break
            count += 1
        return
 
    def suggest_coord(self, word):
        coordlist = []
        glc = -1
        for letter in word.word:
            glc += 1
            rowc = 0
            for row in self.grid:
                rowc += 1
                colc = 0
                for cell in row:
                    colc += 1
                    if letter == cell: # check match letter in word to letters in row
                        try: # vertical
                            if rowc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((rowc - glc) + word.length - 1) <= self.rows: # make sure word doesn't go off the grid
                                    coordlist.append([colc, rowc - glc, 1, 0])
                        except: pass
                        try: # horizontal
                            if colc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((colc - glc) + word.length - 1) <= self.cols: # make sure word doesn't go off the grid
                                    coordlist.append([colc - glc, rowc, 0, 0])
                        except: pass
        new_coordlist = []
        for coord in coordlist:
            col, row, vertical = coord[0], coord[1], coord[2]
            coord[3] = self.check_fit_score(col, row, vertical, word) # checking scores
            if coord[3]: # 0 scores are filtered
                new_coordlist.append(coord)
        random.shuffle(new_coordlist) # randomize coord list; why not?
        new_coordlist.sort(key=lambda i: i[3], reverse=True) # put the best scores first
        return new_coordlist
 
    def fit_and_add(self, word): # doesn't really check fit except for the first word; otherwise just adds if score is good
        fit = False
        count = 0
        coordlist = self.suggest_coord(word)
 
        while not fit and count < self.maxloops:
 
            if len(self.current_word_list) == 0: # this is the first word: the seed
                vertical = random.randrange(0, 2)
                # Place the first word in the middle of the grid
                if vertical:
                    col = int(round((self.cols + 1) / 2, 0))
                    row = int(round((self.rows + 1) / 2, 0)) - int(round((len(word.word) + 1) / 2, 0))
                    if row + len(word.word) > self.rows:
                        row = self.rows - len(word.word) + 1
                else:
                    col = int(round((self.cols + 1) / 2, 0)) - int(round((len(word.word) + 1) / 2, 0))
                    row = int(round((self.rows + 1) / 2, 0))
                    if col + len(word.word) > self.cols:
                        col = self.cols - len(word.word) + 1
 
                if self.check_fit_score(col, row, vertical, word): 
                    fit = True
                    self.set_word(col, row, vertical, word)
            else: # a subsequent words have scores calculated
                try: 
                    col, row, vertical = coordlist[count][0], coordlist[count][1], coordlist[count][2]
                except IndexError: return # no more coordinates, stop trying to fit
 
                if coordlist[count][3]: # already filtered these out, but double check
                    fit = True 
                    self.set_word(col, row, vertical, word)
 
            count += 1
        return
 
    def check_fit_score(self, col, row, vertical, word):
        """Return score (0 means no fit, 1 means a fit, 2+ means a cross)."""
        if col < 1 or row < 1:
            return 0
 
        count, score = 1, 1 # give score a standard value of 1, will override with 0 if collisions detected
        for letter in word.word:            
            try:
                active_cell = self.grid[row-1][col-1]
            except IndexError:
                return 0
            if active_cell == self.empty or active_cell == letter:
                pass
            else:
                return 0
            if active_cell == letter:
                score += 1
            if vertical:
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col+1, row): # check right cell
                        return 0
                    if not self.check_if_cell_clear(col-1, row): # check left cell
                        return 0
                if count == 1: # check top cell only on first letter
                    if not self.check_if_cell_clear(col, row-1):
                        return 0
                if count == len(word.word): # check bottom cell only on last letter
                    if not self.check_if_cell_clear(col, row+1) and row != self.rows:
                        return 0
            else: # else horizontal
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col, row-1): # check top cell
                        return 0
                    if not self.check_if_cell_clear(col, row+1): # check bottom cell
                        return 0
                if count == 1: # check left cell only on first letter
                    if not self.check_if_cell_clear(col-1, row):
                        return 0
                if count == len(word.word): # check right cell only on last letter
                    if not self.check_if_cell_clear(col+1, row) and col != self.cols:
                        return 0
 
            if vertical: # progress to next letter and position
                row += 1
            else: # else horizontal
                col += 1
 
            count += 1
 
        return score
 
    def set_word(self, col, row, vertical, word): # also adds word to word list
        word.col = col
        word.row = row
        word.vertical = vertical
        self.current_word_list.append(word)

        for letter in word.word:
            self.grid[row-1][col-1] = letter
            if vertical:
                row += 1
            else:
                col += 1
        return
 
    def check_if_cell_clear(self, col, row):
        try:
            cell = self.grid[row-1][col-1]
            if cell == self.empty: 
                return True
        except IndexError:
            pass
        return False
 
    def solution(self):
        return '\n'.join([''.join(['{} '.format(c) for c in self.grid[r]]) for r in range(self.rows)])
 
    def order_number_words(self): # orders words and applies numbering system to them
        self.current_word_list.sort(key=lambda i: (i.col))
        self.current_word_list.sort(key=lambda i: (i.row))
        count, icount = 1, 1
        for word in self.current_word_list:
            word.number = count
            if icount < len(self.current_word_list):
                if word.col == self.current_word_list[icount].col and word.row == self.current_word_list[icount].row:
                    pass
                else:
                    count += 1
            icount += 1

    def img_grid(self, name):
        px = 26
        if name.endswith('png'):
            surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 10+(self.cols*px), 10+(self.rows*px))
        else:
            surface = cairo.SVGSurface(name, 10+(self.cols*px), 10+(self.rows*px))
        context = cairo.Context(surface)
        context.set_source_rgb(1, 1, 1)
        context.rectangle(0, 0, 10+(self.cols*px), 10+(self.rows*px))
        context.fill()

        if name.endswith('key.png') or name.endswith('key.svg'):
            for r in range(self.rows):
                for i, c in enumerate(self.grid[r]):
                    if c != '-':
                        context.set_line_width(1.0)
                        context.set_source_rgb(0, 0, 0)
                        context.rectangle(5+(i*px), 5+(r*px), px, px)
                        context.stroke()
                        context.select_font_face('monospace')
                        context.set_font_size(14)
                        context.move_to(5+(i*px)+8, 5+(r*px)+20)
                        context.show_text(c)
        else:
            for r in range(self.rows):
                for i, c in enumerate(self.grid[r]):
                    if c != '-':
                        context.set_line_width(1.0)
                        context.set_source_rgb(0, 0, 0)
                        context.rectangle(5+(i*px), 5+(r*px), px, px)
                        context.stroke()

        self.order_number_words()
        for word in self.current_word_list:
            x, y = 5+((word.col-1)*px), 5+((word.row-1)*px)
            context.select_font_face('monospace')
            context.set_font_size(8)
            context.move_to(x+2, y+9)
            context.show_text(str(word.number))

        if name.endswith('png'):
            surface.write_to_png(name)
        else:
            context.show_page()
            surface.finish()

    def word_bank(self): 
        temp_list = duplicate(self.current_word_list)
        random.shuffle(temp_list)
        return 'Word bank\n' + ''.join(['{}\n'.format(word.word) for word in temp_list])
 
    def legend(self):
        outStrA = '\nClues\nAcross\n'
        outStrD = 'Down\n'
        for word in self.current_word_list:
            if word.down_across() == 'down':
                outStrD += '{:d}. {}\n'.format(word.number, word.clue)
            else:
                outStrA += '{:d}. {}\n'.format(word.number, word.clue)
        return outStrA + outStrD
 
    def clues_txt(self, name):
        clues_file = open(name, 'w')
        clues_file.write(self.word_bank())
        clues_file.write(self.legend())
        clues_file.close()

class Word(object):
    def __init__(self, word=None, clue=None):
        self.word = re.sub(r'\s', '', word.upper())
        self.clue = clue
        self.length = len(self.word)
        # the below are set when placed on board
        self.row = None
        self.col = None
        self.vertical = None
        self.number = None
 
    def down_across(self):
        if self.vertical: 
            return 'down'
        else: 
            return 'across'
 
    def __repr__(self):
        return self.word
