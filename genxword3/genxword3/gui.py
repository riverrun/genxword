# -*- coding: utf-8 -*-

# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2013 David Whitlock
#
# Genxword3-gtk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Genxword3-gtk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with genxword3-gtk.  If not, see <http://www.gnu.org/licenses/gpl.html>.

import os
from gi.repository import Gtk, GtkSource, Pango
from .control import Genxword
from . import calculate

ui_info = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <separator/>
      <menuitem action='Sort'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='CrosswordMenu'>
      <menuitem action='Create'/>
      <menuitem action='Incgsize'/>
      <menuitem action='Save'/>
      <separator/>
      <menuitem action='EditGsize'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='Help'/>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='New'/>
    <toolitem action='Open'/>
    <separator action='Sep1'/>
    <toolitem action='Create'/>
    <toolitem action='Incgsize'/>
    <separator action='Sep2'/>
    <toolitem action='Save'/>
    <separator action='Sep3'/>
    <toolitem action='Help'/>
  </toolbar>
</ui>
"""

class Genxinterface(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='genxword3-gtk')

        self.set_default_size(650, 550)
        self.set_default_icon_name('genxword3-gtk')
        self.saveformat = ''
        self.gsize = False

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_border_width(6)
        self.grid.set_row_spacing(6)
        self.grid.set_column_spacing(6)

        action_group = Gtk.ActionGroup('gui_actions')
        self.add_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget('/MenuBar')
        self.grid.attach(menubar, 0, 0, 6, 1)
        toolbar = uimanager.get_widget('/ToolBar')
        self.grid.attach(toolbar, 0, 1, 6, 1)

        self.notebk()
        self.save_buttons()
        self.option_buttons()

        self.list_clickable_buttons(uimanager)
        self.set_sensitivities(True)

    def add_actions(self, action_group):
        action_group.add_actions([
            ('FileMenu', None, '_Word list'),
            ('New', Gtk.STOCK_NEW, '_New word list', None, 
                'Create a new word list or go back to the already open word list', self.new_wlist),
            ('Open', Gtk.STOCK_OPEN, '_Open word list', None, 'Open a word list', self.open_wlist),
            ('Sort', None, '_Sort word list', None, 
                'Sort the word list and remove words with non-alphabetic characters', self.sort_wlist),
            ('Quit', Gtk.STOCK_QUIT, 'Quit', None, 'Quit', self.quit_app),
            ('CrosswordMenu', None, '_Crossword'),
            ('Create', Gtk.STOCK_EXECUTE, '_Calculate crossword', '<Ctrl>G', 
                'Calculate the crossword', self.create_xword),
            ('Incgsize', Gtk.STOCK_ADD, '_Recalculate', '<Ctrl>R', 
                'Increase the grid size and recalculate the crossword', self.incgsize),
            ('Save', Gtk.STOCK_SAVE, '_Save', None, 'Save crossword', self.save_xword),
            ('HelpMenu', None, '_Help'),
            ('Help', Gtk.STOCK_HELP, '_Help', 'F1', 'Open the help page', self.help_page),
            ('About', Gtk.STOCK_ABOUT, '_About', None, 'About', self.about_dialog)
            ])

        edit_gsize = Gtk.ToggleAction('EditGsize', 'Choose the grid size', None, None)
        edit_gsize.connect('toggled', self.set_gsize)
        action_group.add_action(edit_gsize)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(ui_info)
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def notebk(self):
        self.notebk_win = Gtk.Notebook()
        self.notebk_win.set_show_tabs(False)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview_win(scrolledwindow)
        self.notebk_win.append_page(scrolledwindow, None)

        xwordwindow = Gtk.ScrolledWindow()
        xwordwindow.set_hexpand(True)
        xwordwindow.set_vexpand(True)
        self.xword_label = Gtk.Label()
        self.xword_label.set_margin_left(6)
        self.xword_label.set_margin_right(6)
        xwordwindow.add_with_viewport(self.xword_label)
        self.notebk_win.append_page(xwordwindow, None)
        self.grid.attach(self.notebk_win, 0, 2, 6, 1)

    def textview_win(self, wordlist_win):
        self.textview = GtkSource.View.new()
        self.textview.set_show_line_numbers(True)
        self.textview.set_border_width(6)
        fontdesc = Pango.FontDescription('serif 11')
        self.textview.modify_font(fontdesc)
        self.buff = self.textview.get_buffer()
        wordlist_win.add(self.textview)

        manager = GtkSource.LanguageManager()
        path = manager.get_search_path()
        path.extend(['/usr/share/genxword3', '/usr/local/share/genxword3'])
        manager.set_search_path(path)
        lang = manager.get_language('gumby')
        self.buff.set_language(lang)

    def save_buttons(self):
        save_bar = Gtk.ButtonBox()
        self.grid.attach(save_bar, 0, 3, 6, 1)

        save_label = Gtk.Label('Save the crossword as')
        save_bar.add(save_label)

        save_A4 = Gtk.CheckButton('A4 pdf')
        save_A4.connect('toggled', self.save_options, 'p')
        save_bar.add(save_A4)

        save_letter = Gtk.CheckButton('letter pdf')
        save_letter.connect('toggled', self.save_options, 'l')
        save_bar.add(save_letter)

        save_png = Gtk.CheckButton('png')
        save_png.connect('toggled', self.save_options, 'n')
        save_bar.add(save_png)

        save_svg = Gtk.CheckButton('svg')
        save_svg.connect('toggled', self.save_options, 's')
        save_bar.add(save_svg)

    def option_buttons(self):
        self.enter_name = Gtk.Entry()
        self.enter_name.set_text('Name of crossword')
        self.enter_name.set_tooltip_text('Choose the name of your crossword')
        self.enter_name.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_CLEAR)
        self.enter_name.connect('icon-press', self.entry_cleared)
        self.grid.attach(self.enter_name, 0, 4, 2, 1)

        nwords_label = Gtk.Label('Number of words')
        self.grid.attach(nwords_label, 2, 4, 1, 1)

        adjustment = Gtk.Adjustment(50, 10, 500, 5, 10, 0)
        self.choose_nwords = Gtk.SpinButton()
        self.choose_nwords.set_adjustment(adjustment)
        self.choose_nwords.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.choose_nwords.set_tooltip_text('Choose the number of words you want to use')
        self.grid.attach(self.choose_nwords, 3, 4, 1, 1)

        gsize_label = Gtk.Label('Grid size')
        self.grid.attach(gsize_label, 4, 4, 1, 1)

        self.choose_gsize = Gtk.Entry()
        self.choose_gsize.set_text('17,17')
        self.choose_gsize.set_width_chars(8)
        gsize_tip = 'Choose the crossword grid size\nGo to the Crossword menu to enable this option'
        self.choose_gsize.set_tooltip_text(gsize_tip)
        self.choose_gsize.set_sensitive(False)
        self.grid.attach(self.choose_gsize, 5, 4, 1, 1)

    def list_clickable_buttons(self, uimanager):
        self.click_buttons = []
        self.click_buttons.append(uimanager.get_widget('/MenuBar/FileMenu/Sort'))
        unclick_list = ['/MenuBar/CrosswordMenu/Incgsize', '/MenuBar/CrosswordMenu/Save', 
            '/ToolBar/Incgsize', '/ToolBar/Save']
        self.unclick_buttons = [uimanager.get_widget(name) for name in unclick_list]

    def set_sensitivities(self, value, page=0):
        for button in self.click_buttons:
            button.set_sensitive(value)
        for button in self.unclick_buttons:
            button.set_sensitive(not value)
        self.notebk_win.set_current_page(page)
        self.calc_first_time = value

    def entry_cleared(self, entry, position, event):
        self.enter_name.set_text('')
        self.enter_name.grab_focus()

    def save_options(self, button, name):
        if button.get_active():
            self.saveformat += name
        else:
            self.saveformat = self.saveformat.replace(name, '')

    def new_wlist(self, button):
        self.set_sensitivities(True, 0)

    def open_wlist(self, button):
        dialog = Gtk.FileChooserDialog('Please choose a file', self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename()) as infile:
                data = infile.read()
            self.buff.set_text(data)
        dialog.destroy()
        self.set_sensitivities(True, 0)

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('Text files')
        filter_text.add_mime_type('text/plain')
        dialog.add_filter(filter_text)

    def sort_wlist(self, button):
        data = self.buff.get_text(self.buff.get_start_iter(), self.buff.get_end_iter(), False)
        valid = [[word for word in line.split(' ', 1)] for line in data.splitlines() if line.split(' ', 1)[0].isalpha()]
        valid.sort(key=lambda i: len(i[0]))
        output = '\n'.join([' '.join(word) for word in valid])
        self.buff.set_text(output)

    def create_xword(self, button):
        if self.calc_first_time:
            self.words = self.buff.get_text(self.buff.get_start_iter(), self.buff.get_end_iter(), False)
            nwords = self.choose_nwords.get_value_as_int()
            gen = Genxword()
            gen.wlist(self.words.splitlines(), nwords)
            self.wlist = gen.word_list
            gen.grid_size(True)
            if self.gsize:
                gen.check_grid_size(self.choose_gsize.get_text())
            self.nrow, self.ncol = gen.nrow, gen.ncol
            self.calc_xword()
            self.set_sensitivities(False, 1)
        else:
            self.calc_xword()

    def calc_xword(self):
        calc = calculate.Crossword(self.nrow, self.ncol, ' ', self.wlist)
        display = '<span font="monospace bold 11">' + calc.compute_crossword() + '</span>'
        self.xword_label.set_markup(display)
        self.xword_view(False, Gtk.Align.FILL)
        self.choose_gsize.set_text(str(self.nrow) + ',' + str(self.ncol))
        self.best_word_list = calc.best_word_list
        self.best_grid = calc.best_grid

    def incgsize(self, button):
        self.nrow += 2;self.ncol += 2
        self.calc_xword()

    def xword_view(self, value, alignment):
        self.xword_label.set_line_wrap(value)
        self.xword_label.set_valign(alignment)
        self.xword_label.set_halign(alignment)

    def set_gsize(self, button):
        self.gsize = button.get_active()
        self.choose_gsize.set_sensitive(button.get_active())

    def save_xword(self, button):
        self.xwordname = self.enter_name.get_text()
        if self.xwordname != 'Name of crossword' and self.saveformat:
            dialog = Gtk.FileChooserDialog('Please choose a folder', self,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 'Select', Gtk.ResponseType.OK))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                os.chdir(dialog.get_filename())
            else:
                dialog.destroy()
                return 0
            dialog.destroy()
            exp = calculate.Exportfiles(self.nrow, self.ncol, self.best_grid, self.best_word_list)
            exp.create_files(self.xwordname, self.saveformat, True)
            with open(self.xwordname + '_wlist.txt', 'w') as wlist_file:
                wlist_file.write(self.words)
            text = 'Your crossword files have been saved in ' + os.getcwd()
            self.enter_name.set_text('Name of crossword')
            self.buff.set_text('')
        else:
            text = ('Please fill in the name of the crossword and the format you want it saved in '
                    '(A4 size pdf, letter size pdf, png or svg).\nThen click on the Save button again.')
        display = '<span font="serif 11">' + text + '</span>'
        self.xword_label.set_markup(display)
        self.xword_view(True, Gtk.Align.START)

    def help_page(self, button):
        if os.path.isfile('/usr/share/genxword3/help_page'):
            with open('/usr/share/genxword3/help_page') as help_file:
                text = help_file.read()
        else:
            with open('/usr/local/share/genxword3/help_page') as help_file:
                text = help_file.read()
        self.xword_label.set_markup(text)
        self.xword_view(True, Gtk.Align.START)
        self.notebk_win.set_current_page(1)

    def about_dialog(self, button):
        license = ('Genxword3-gtk is free software: you can redistribute it and/or modify'
        'it under the terms of the GNU General Public License as published by'
        'the Free Software Foundation, either version 3 of the License, or'
        '(at your option) any later version.\n\n'
        'Genxword3-gtk is distributed in the hope that it will be useful,'
        'but WITHOUT ANY WARRANTY; without even the implied warranty of'
        'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the'
        'GNU General Public License for more details.\n\n'
        'You should have received a copy of the GNU General Public License'
        'along with genxword3-gtk.  If not, see http://www.gnu.org/licenses/gpl.html')
        about = Gtk.AboutDialog()
        about.set_program_name('genxword3-gtk')
        about.set_version('0.9.5')
        about.set_license(license)
        about.set_wrap_license(True)
        about.set_comments('A crossword generator')
        about.set_authors(['David Whitlock <alovedalongthe@gmail.com>', 'Bryan Helmig'])
        about.set_website('https://github.com/riverrun/genxword/wiki/genxword-gtk')
        about.set_website_label('genxword3-gtk wiki')
        about.set_logo_icon_name('genxword3-gtk')
        about.run()
        about.destroy()

    def quit_app(self, widget):
        Gtk.main_quit()

def main():
    win = Genxinterface()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
