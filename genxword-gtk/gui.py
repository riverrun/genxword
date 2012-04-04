#!/usr/bin/python2.7

import os, random
from gi.repository import Gtk, Pango
from gencrossword import calcxword

help_text = """Help, I need somebody!"""

class GXinterface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='genxword-gtk')

        self.set_default_size(-1, 350)
        self.saveformat = ''

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.textview_win()
        self.check_buttons()
        self.tool_buttons()

    def textview_win(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 6, 1)

        self.textview = Gtk.TextView()
        fontdesc = Pango.FontDescription('monospace')
        self.textview.modify_font(fontdesc)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(help_text)
        scrolledwindow.add(self.textview)

    def check_buttons(self):
        label = Gtk.Label('Save options')
        self.grid.attach(label, 0, 2, 1, 1)

        save_A4pdf = Gtk.CheckButton('A4 pdf')
        save_A4pdf.set_active(False)
        save_A4pdf.connect('toggled', self.save_A4pdf_toggled)
        self.grid.attach(save_A4pdf, 1, 2, 1, 1)

        save_letterpdf = Gtk.CheckButton('letter pdf')
        save_letterpdf.set_active(False)
        save_letterpdf.connect('toggled', self.save_letterpdf_toggled)
        self.grid.attach(save_letterpdf, 2, 2, 1, 1)

        save_png = Gtk.CheckButton('png')
        save_png.set_active(False)
        save_png.connect('toggled', self.save_png_toggled)
        self.grid.attach(save_png, 3, 2, 1, 1)

        save_svg = Gtk.CheckButton('svg')
        save_svg.set_active(False)
        save_svg.connect('toggled', self.save_svg_toggled)
        self.grid.attach(save_svg, 4, 2, 1, 1)

    def save_A4pdf_toggled(self, widget):
        if widget.get_active():
            self.saveformat += 'p'

    def save_letterpdf_toggled(self, widget):
        if widget.get_active():
            self.saveformat += 'l'

    def save_png_toggled(self, widget):
        if widget.get_active():
            self.saveformat += 'n'

    def save_svg_toggled(self, widget):
        if widget.get_active():
            self.saveformat += 's'

    def tool_buttons(self):
        button_new = Gtk.Button(stock=Gtk.STOCK_NEW)
        button_new.connect('clicked', self.new_wlist)
        self.grid.attach(button_new, 0, 0, 1, 1)

        button_open = Gtk.Button(stock=Gtk.STOCK_OPEN)
        button_open.connect('clicked', self.open_wlist)
        self.grid.attach(button_open, 1, 0, 1, 1)

        button_calc = Gtk.Button('_Calculate', use_underline=True)
        button_calc.connect('clicked', self.calc_xword)
        self.grid.attach(button_calc, 2, 0, 1, 1)

        button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)
        button_save.connect('clicked', self.save_xword)
        self.grid.attach(button_save, 3, 0, 1, 1)

        button_help = Gtk.Button(stock=Gtk.STOCK_HELP)
        button_help.connect('clicked', self.help_page)
        self.grid.attach(button_help, 4, 0, 1, 1)

        button_quit = Gtk.Button(stock=Gtk.STOCK_QUIT)
        button_quit.connect('clicked', Gtk.main_quit)
        self.grid.attach(button_quit, 5, 0, 1, 1)

    def new_wlist(self, button):
        self.textview.set_editable(True)
        self.textview.set_cursor_visible(True)
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
            self.textbuffer.set_text(data)
        elif response == Gtk.ResponseType.CANCEL:
            print 'Cancel clicked'

        dialog.destroy()

    def calc_xword(self, button):
        buff = self.textview.get_buffer() # find better way of saving wordlist
        rawtext = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)
        with open('/tmp/genxwordlist', 'w') as wlist_file:
            wlist_file.write(rawtext)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.wlist()
        self.grid_size()
        self.gengrid()

    def gengrid(self):
        a = calcxword.Crossword(self.ncol, self.nrow, '-', self.word_list)
        a.compute_crossword()
        self.textbuffer.set_text(a.solution())
        self.textbuffer.insert_at_cursor('\n' + str(len(a.current_word_list)) + ' out of ' + str(len(self.word_list)))
        os.chdir('/tmp')
        a.create_files('Gumby', self.saveformat)

    def save_xword(self, button):
        dialog = Gtk.FileChooserDialog('Please choose a folder', self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             'Select', Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            os.chdir(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print 'Cancel clicked'

        dialog.destroy()

    def help_page(self, button):
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textbuffer.set_text(help_text)

    def wlist(self):
        with open('/tmp/genxwordlist') as infile:
            self.word_list = [line.strip().split(' ', 1) for line in infile if line.strip()]
        if len(self.word_list) > 50:
            self.word_list = random.sample(self.word_list, 50)

    def grid_size(self):
        if len(self.word_list) <= 20:
            self.ncol = self.nrow = 17
        elif len(self.word_list) <= 100:
            self.ncol = self.nrow = int((round(((len(self.word_list) - 20) / 7.5), 0) * 2) + 19)
        else:
            self.ncol = self.nrow = 43

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name('Text files')
        filter_text.add_mime_type('text/plain')
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('Any files')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

win = GXinterface()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
