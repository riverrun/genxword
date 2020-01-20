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

import os
import sys
import gettext
import random
from .calculate import Crossword, Exportfiles
from .complexstring import ComplexString

base_dir = os.path.abspath(os.path.dirname(__file__))
d = '/usr/local/share' if 'local' in base_dir.split('/') else '/usr/share'
gettext.bindtextdomain('genxword', os.path.join(d, 'locale'))
gettext.textdomain('genxword')
_ = gettext.gettext

class Genxword(object):
    def __init__(self, auto=False, mixmode=False):
        self.auto = auto
        self.mixmode = mixmode

    def wlist(self, words, nwords=50):
        """Create a list of words and clues."""
        wordlist = [line.strip().split(' ', 1) for line in words if line.strip()]
        if len(wordlist) > nwords:
            wordlist = random.sample(wordlist, nwords)
        self.wordlist = [[ComplexString(line[0].upper()), line[-1]] for line in wordlist]
        self.wordlist.sort(key=lambda i: len(i[0]), reverse=True)
        if self.mixmode:
            for line in self.wordlist:
                line[1] = self.word_mixer(line[0].lower())

    def word_mixer(self, word):
        """Create anagrams for the clues."""
        word = orig_word = list(word)
        for i in range(3):
            random.shuffle(word)
            if word != orig_word:
                break
        return ''.join(word)

    def grid_size(self, gtkmode=False):
        """Calculate the default grid size."""
        if len(self.wordlist) <= 20:
            self.nrow = self.ncol = 17
        elif len(self.wordlist) <= 100:
            self.nrow = self.ncol = int((round((len(self.wordlist) - 20) / 8.0) * 2) + 19)
        else:
            self.nrow = self.ncol = 41
        if min(self.nrow, self.ncol) <= len(self.wordlist[0][0]):
            self.nrow = self.ncol = len(self.wordlist[0][0]) + 2
        if not gtkmode and not self.auto:
            gsize = str(self.nrow) + ', ' + str(self.ncol)
            grid_size = input(_('Enter grid size (') + gsize + _(' is the default): '))
            if grid_size:
                self.check_grid_size(grid_size)

    def check_grid_size(self, grid_size):
        try:
            nrow, ncol = int(grid_size.split(',')[0]), int(grid_size.split(',')[1])
        except:
            pass
        else:
            if len(self.wordlist[0][0]) < min(nrow, ncol):
                self.nrow, self.ncol = nrow, ncol

    def gengrid(self, name, saveformat):
        i = 0
        while 1:
            print(_('Calculating your crossword...'))
            calc = Crossword(self.nrow, self.ncol, '-', self.wordlist)
            print(calc.compute_crossword())
            if self.auto:
                if float(len(calc.best_wordlist))/len(self.wordlist) < 0.9 and i < 5:
                    self.nrow += 2; self.ncol += 2
                    i += 1
                else:
                    break
            else:
                h = input(_('Are you happy with this solution? [Y/n] '))
                if h.strip() != _('n'):
                    break
                inc_gsize = input(_('And increase the grid size? [Y/n] '))
                if inc_gsize.strip() != _('n'):
                    self.nrow += 2;self.ncol += 2
        lang = _('Across/Down').split('/')
        message = _('The following files have been saved to your current working directory:\n')
        exp = Exportfiles(self.nrow, self.ncol, calc.best_grid, calc.best_wordlist, '-')
        exp.create_files(name, saveformat, lang, message)
