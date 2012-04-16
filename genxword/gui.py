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

import os, tempfile
from gi.repository import Gtk, Pango
from . import calculate
from .control import Genxword

help_text = """genxword-gtk
Genxword-gtk is a crossword generator, which produces pdf (A4 or letter size) versions of the grid and clues, \
or png / svg versions of the crossword grid, together with a text file containing the words and clues.\n
New word list
You can create a new word list by clicking on the 'new' button, or by pressing Control + N. \
The word list can be just a list of words, like this:\n
parrot
spam
vikings\n
or it can be a list or words and clues, like this:\n
excalibur A sword that a moistened bint lobbed at Arthur.
duck An animal that weighs the same as a witch.
coconut A fruit that possibly migrates.\n
As you can see, each word needs to be on a separate line, and there should be a space between each word and its clue. \
The clue is everything after the first space.\n
Open word list
Clicking the 'open' button, or pressing Control + O, lets you open, and edit, a word list, which needs to be \
formatted as written above. The word list can be thousands of words long, and the crossword will be created \
with a set amount of words randomly selected from it. The default number of words is 50.\n
Calculate - create the crossword
Click on the 'create' button, or press Control + G, to create the crossword. If you click on it a second time, \
the crossword will be recalculated.\n
Increase grid size - increase the grid size and recalculate
Clicking on this button, or pressing Control + R, increases the grid size before recalculating the crossword.\n
Save - save the crossword
This button, or Control + S, lets you choose where you save the crossword files.\n
Further options
You can save the crossword in pdf, png and / or svg format. Just click on the appropriate entries in the 'Save options' menu.
On the bottom row of this window, there are boxes in which you can write the name of the crossword, choose the number \
of words used, and choose the grid size. To change the grid size, you will need to enable this option in the 'Crossword' \
menu first (normally, the grid size will be automatically calculated based on the number of words used). \
The numbers in the grid size box refer to the number of columns and rows, and they need to be separated by a comma.
"""
save_recalc = """\nIf you want to save this crossword, press the Save button.
If you want to recalculate the crossword, press the Calculate button.
To increase the grid size and then recalculate the crossword, 
press the Inc grid size button.
"""

ui_info = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
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
    <menu action='SaveOptsMenu'>
      <menuitem action='SaveA4'/>
      <menuitem action='Saveletter'/>
      <menuitem action='Savepng'/>
      <menuitem action='Savesvg'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='Help'/>
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
        Gtk.Window.__init__(self, title='genxword-gtk')

        self.set_default_size(650, 450)
        self.saveformat = ''
        self.gsize = False

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.set_border_width(6)
        self.grid.set_row_spacing(6)
        self.grid.set_column_spacing(6)

        action_group = Gtk.ActionGroup('main_actions')
        self.add_main_actions(action_group)
        self.add_opts_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget('/MenuBar')
        self.grid.attach(menubar, 0, 0, 6, 1)
        toolbar = uimanager.get_widget('/ToolBar')
        self.grid.attach(toolbar, 0, 1, 6, 1)

        self.textview_win()
        self.bottom_row()
        self.win_icon()

    def add_main_actions(self, action_group):
        action_filemenu = Gtk.Action('FileMenu', '_Word list', None, None)
        action_group.add_action(action_filemenu)

        action_xwordmenu = Gtk.Action('CrosswordMenu', '_Crossword', None, None)
        action_group.add_action(action_xwordmenu)

        action_helpmenu = Gtk.Action('HelpMenu', '_Help', None, None)
        action_group.add_action(action_helpmenu)

        action_new = Gtk.Action('New', 'New word list', 'Create a new word list', Gtk.STOCK_NEW)
        action_new.connect('activate', self.new_wlist)
        action_group.add_action_with_accel(action_new, None)

        action_open = Gtk.Action('Open', 'Open word list', 'Open an existing word list', Gtk.STOCK_OPEN)
        action_open.connect('activate', self.open_wlist)
        action_group.add_action_with_accel(action_open, None)

        action_create = Gtk.Action('Create', 'Create crossword', 'Calculate the crossword', Gtk.STOCK_EXECUTE)
        action_create.connect('activate', self.calc_xword)
        action_group.add_action_with_accel(action_create, '<control>G')

        action_incgsize = Gtk.Action('Incgsize', 'Increase grid size',
            'Increase the grid size and recalculate the crossword', Gtk.STOCK_REDO)
        action_incgsize.connect('activate', self.incgsize)
        action_group.add_action_with_accel(action_incgsize, '<control>R')

        action_save = Gtk.Action('Save', 'Save', 'Save crossword', Gtk.STOCK_SAVE)
        action_save.connect('activate', self.save_xword)
        action_group.add_action_with_accel(action_save, None)

        action_help = Gtk.Action('Help', 'Help', 'Help page', Gtk.STOCK_HELP)
        action_help.connect('activate', self.help_page)
        action_group.add_action_with_accel(action_help, None)

        action_quit = Gtk.Action('Quit', 'Quit', None, Gtk.STOCK_QUIT)
        action_quit.connect('activate', self.quit_app)
        action_group.add_action_with_accel(action_quit, None)

    def add_opts_actions(self, action_group):
        action_optsmenu = Gtk.Action('SaveOptsMenu', '_Save options', None, None)
        action_group.add_action(action_optsmenu)
        save_A4 = Gtk.ToggleAction('SaveA4', 'Save as A4 pdf', None, None)
        save_A4.connect('toggled', self.save_options, 'p')
        action_group.add_action(save_A4)
        save_letter = Gtk.ToggleAction('Saveletter', 'Save as letter pdf', None, None)
        save_letter.connect('toggled', self.save_options, 'l')
        action_group.add_action(save_letter)
        save_png = Gtk.ToggleAction('Savepng', 'Save as png', None, None)
        save_png.connect('toggled', self.save_options, 'n')
        action_group.add_action(save_png)
        save_svg = Gtk.ToggleAction('Savesvg', 'Save as svg', None, None)
        save_svg.connect('toggled', self.save_options, 's')
        action_group.add_action(save_svg)
        edit_gsize = Gtk.ToggleAction('EditGsize', 'Choose the grid size', None, None)
        edit_gsize.connect('toggled', self.set_gsize)
        action_group.add_action(edit_gsize)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(ui_info)
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def textview_win(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 2, 6, 1)

        self.textview = Gtk.TextView()
        self.textview.set_border_width(6)
        fontdesc = Pango.FontDescription('serif')
        self.textview.modify_font(fontdesc)
        self.textbuffer = self.textview.get_buffer()
        self.tag_title = self.textbuffer.create_tag('title', font='sans bold 12')
        self.tag_subtitle = self.textbuffer.create_tag('subtitle', font='sans bold')
        self.tag_mono = self.textbuffer.create_tag('mono', font='monospace')
        self.help_message()
        scrolledwindow.add(self.textview)

    def bottom_row(self):
        self.enter_name = Gtk.Entry()
        self.enter_name.set_text('Name of crossword')
        self.enter_name.set_tooltip_text('Choose the name of your crossword')
        self.enter_name.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_CLEAR)
        self.enter_name.connect('icon-press', self.entry_cleared)
        self.grid.attach(self.enter_name, 0, 3, 2, 1)

        nwords_label = Gtk.Label('Number of words')
        self.grid.attach(nwords_label, 2, 3, 1, 1)

        adjustment = Gtk.Adjustment(50, 10, 500, 5, 10, 0)
        self.choose_nwords = Gtk.SpinButton()
        self.choose_nwords.set_adjustment(adjustment)
        self.choose_nwords.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.choose_nwords.set_tooltip_text('Choose the number of words you want to use')
        self.grid.attach(self.choose_nwords, 3, 3, 1, 1)

        gsize_label = Gtk.Label('Grid size')
        self.grid.attach(gsize_label, 4, 3, 1, 1)

        self.choose_gsize = Gtk.Entry()
        self.choose_gsize.set_text('17,17')
        gsize_tip = 'Choose the crossword grid size\nGo to the Crossword menu to enable this option'
        self.choose_gsize.set_tooltip_text(gsize_tip)
        self.choose_gsize.set_sensitive(False)
        self.grid.attach(self.choose_gsize, 5, 3, 1, 1)

    def entry_cleared(self, entry, position, event):
        self.enter_name.set_text('')
        self.enter_name.grab_focus()

    def save_options(self, button, name):
        if button.get_active():
            self.saveformat += name
        else:
            self.saveformat = self.saveformat.replace(name, '')

    def win_icon(self):
        try:
            self.set_icon_from_file('/usr/share/pixmaps/genxword-gtk.png')
        except:
            pass

    def new_wlist(self, button):
        self.textview.set_editable(True)
        self.textview.set_cursor_visible(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        self.textbuffer.set_text('')

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
            self.textview.set_editable(True)
            self.textview.set_cursor_visible(True)
            self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
            self.textbuffer.set_text(data)
        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('Text files')
        filter_text.add_mime_type('text/plain')
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('Any files')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

    def calc_xword(self, button):
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        buff = self.textview.get_buffer()
        rawtext = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
        if save_recalc in rawtext:
            self.textbuffer.set_text(self.gen.calcgrid())
            self.add_tag(self.tag_mono, 0, -1)
            self.textbuffer.insert_at_cursor(save_recalc)
        else:
            fd, wordlist = tempfile.mkstemp()
            with open(wordlist, 'w') as wlist_file:
                wlist_file.write(rawtext)
            self.textview.set_editable(False)
            self.textview.set_cursor_visible(False)
            nwords = self.choose_nwords.get_value_as_int()
            self.gen = Genxword()
            with open(wordlist) as infile:
                self.gen.wlist(infile, nwords)
            self.gen.grid_size(True)
            if self.gsize:
                self.gen.check_grid_size(self.choose_gsize.get_text())
            self.textbuffer.set_text(self.gen.calcgrid())
            self.add_tag(self.tag_mono, 0, -1)
            self.textbuffer.insert_at_cursor(save_recalc)
            os.close(fd)
            os.remove(wordlist)

    def incgsize(self, button):
        self.textview.set_wrap_mode(Gtk.WrapMode.NONE)
        self.textbuffer.set_text(self.gen.calcgrid(True))
        self.add_tag(self.tag_mono, 0, -1)
        self.textbuffer.insert_at_cursor(save_recalc)

    def set_gsize(self, button):
        if button.get_active():
            self.gsize = True
            self.choose_gsize.set_sensitive(True)
        else:
            self.gsize = False
            self.choose_gsize.set_sensitive(False)

    def save_xword(self, button):
        self.xwordname = self.enter_name.get_text()
        if self.saveformat and self.xwordname != 'Name of crossword':
            dialog = Gtk.FileChooserDialog('Please choose a folder', self,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 'Select', Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                os.chdir(dialog.get_filename())
            dialog.destroy()

            self.gen.savefiles(self.saveformat, self.xwordname, True)
            saved_message = 'Your crossword files have been saved in ' + os.getcwd()
            self.textbuffer.set_text(saved_message)
            self.enter_name.set_text('Name of crossword')
        else:
            self.textbuffer.set_text('Please fill in the name of the crossword and how you want it saved.')
            self.textbuffer.insert_at_cursor('\nThen click on the Save button again.')

    def help_page(self, button):
        self.help_message()

    def help_message(self):
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textbuffer.set_text(help_text)
        self.add_tag(self.tag_title, 0, 1)
        self.add_tag(self.tag_subtitle, 3, 4)
        self.add_tag(self.tag_subtitle, 18, 19)
        self.add_tag(self.tag_subtitle, 21, 22)
        self.add_tag(self.tag_subtitle, 24, 25)
        self.add_tag(self.tag_subtitle, 27, 28)
        self.add_tag(self.tag_subtitle, 30, 31)

    def add_tag(self, tag_name, startline, endline):
        start = self.textbuffer.get_iter_at_line(startline)
        end = self.textbuffer.get_iter_at_line(endline)
        self.textbuffer.apply_tag(tag_name, start, end)

    def quit_app(self, widget):
        Gtk.main_quit()

def main():
    win = Genxinterface()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
