# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2014 David Whitlock
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
from . import calculate

PY2 = sys.version_info[0] == 2
if PY2:
    input = raw_input
    chr = unichr
    calculate.Exportfiles.word_bank = calculate.Exportfiles.old_word_bank
    calculate.Exportfiles.legend = calculate.Exportfiles.old_legend

base_dir = os.path.abspath(os.path.dirname(__file__))
d = '/usr/local/share' if 'local' in base_dir.split('/') else '/usr/share'
gettext.bindtextdomain('genxword', os.path.join(d, 'locale'))
if PY2:
    gettext.bind_textdomain_codeset('genxword', codeset='utf-8')
gettext.textdomain('genxword')
_ = gettext.gettext

usage_info = _("""The word list file contains the words and clues, or just words, that you want in your crossword. 
For further information on how to format the word list file and about the other options, please consult the man page.
""")

class Genxword(object):
    def __init__(self, auto=False, mixmode=False):
        self.auto = auto
        self.mixmode = mixmode
        self.Thai = False

    def thai_set(self):
        """Handle Thai (superscript / subscript) characters."""
        self.Thai = True
        code_list = [3633, 3636, 3637, 3638, 3639, 3640, 3641, 3655, 3656, 3657, 3658,
                3659, 3660, 3661, 3662]
        chars = {chr(n) for n in code_list}
        for line in self.word_list:
            skip = []
            for letter in line[0]:
                if letter in chars:
                    skip[-1] += letter
                    continue
                skip.append(letter)
            line[0] = skip

    def wlist(self, infile, nwords=50):
        """Create a list of words and clues."""
        if PY2:
            word_list = [line.decode('utf-8', 'ignore').strip().split(' ', 1) for line in infile if line.strip()]
        else:
            word_list = [line.strip().split(' ', 1) for line in infile if line.strip()]
        if len(word_list) > nwords:
            word_list = random.sample(word_list, nwords)
        self.word_list = [[line[0].upper(), line[-1]] for line in word_list]
        if 3584 < ord(self.word_list[0][0][0]) < 3676:
            self.thai_set()
        self.word_list.sort(key=lambda i: len(i[0]), reverse=True)
        if self.mixmode:
            for line in self.word_list:
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
        if len(self.word_list) <= 20:
            self.nrow = self.ncol = 17
        elif len(self.word_list) <= 100:
            self.nrow = self.ncol = int((round((len(self.word_list) - 20) / 8.0) * 2) + 19)
        else:
            self.nrow = self.ncol = 41
        if min(self.nrow, self.ncol) <= len(self.word_list[0][0]):
            self.nrow = self.ncol = len(self.word_list[0][0]) + 2
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
            if len(self.word_list[0][0]) < min(nrow, ncol):
                self.nrow, self.ncol = nrow, ncol

    def gengrid(self, name, saveformat):
        i = 0
        while 1:
            print(_('Calculating your crossword...'))
            calc = calculate.Crossword(self.nrow, self.ncol, '-', self.word_list)
            print(calc.compute_crossword())
            if self.auto:
                if float(len(calc.best_word_list))/len(self.word_list) < 0.9 and i < 5:
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
        exp = calculate.Exportfiles(self.nrow, self.ncol, calc.best_grid, calc.best_word_list, '-')
        exp.create_files(name, saveformat, lang, message, self.Thai)

def main():
    import argparse
    parser = argparse.ArgumentParser(description=_('Crossword generator.'), prog='genxword', epilog=usage_info)
    parser.add_argument('infile', type=argparse.FileType('r'), help=_('Name of word list file.'))
    parser.add_argument('saveformat', help=_('Save files as A4 pdf (p), letter size pdf (l), png (n) and/or svg (s).'))
    parser.add_argument('-a', '--auto', dest='auto', action='store_true', help=_('Automated (non-interactive) option.'))
    parser.add_argument('-m', '--mix', dest='mixmode', action='store_true', help=_('Create anagrams for the clues'))
    parser.add_argument('-n', '--number', dest='nwords', type=int, default=50, help=_('Number of words to be used.'))
    parser.add_argument('-o', '--output', dest='output', default='Gumby', help=_('Name of crossword.'))
    args = parser.parse_args()
    gen = Genxword(args.auto, args.mixmode)
    gen.wlist(args.infile, args.nwords)
    gen.grid_size()
    gen.gengrid(args.output, args.saveformat)
