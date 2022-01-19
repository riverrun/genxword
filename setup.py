# Authors: David Whitlock <alovedalongthe@gmail.com>, Bryan Helmig
# Crossword generator that outputs the grid and clues as a pdf file and/or
# the grid in png/svg format with a text file containing the words and clues.
# Copyright (C) 2010-2011 Bryan Helmig
# Copyright (C) 2011-2016 David Whitlock
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
import subprocess
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

def add_data():
    try:
        data_files = [('share/applications', ['extra/genxword-gtk.desktop']),
                ('share/pixmaps', ['extra/genxword-gtk.png'])]
        if not os.path.isdir('mo'):
            os.mkdir('mo')
        for pofile in os.listdir('po'):
            if pofile.endswith('po'):
                lang = pofile.strip('.po')
                modir = os.path.join('mo', lang)
                if not os.path.isdir(modir):
                    os.mkdir(modir)
                mofile = os.path.join(modir, 'genxword.mo')
                subprocess.call('msgfmt {} -o {}'.format(os.path.join('po', pofile), mofile), shell=True)
                data_files.append(['share/locale/{}/LC_MESSAGES/'.format(lang), [mofile]])
        return data_files
    except:
        return

if os.name == 'posix':
    data_files = add_data()
else:
    data_files = None

setup(
    name='genxword',
    version='2.2.0',
    author='David Whitlock',
    author_email='alovedalongthe@gmail.com',
    url='https://github.com/riverrun/genxword',
    description='A crossword generator',
    long_description=long_description,
    license='GPLv3',
    packages=['genxword'],
    include_package_data=True,
    data_files=data_files,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Office/Business',
    ],
    install_requires=[
    	'pycairo',
    	'PyGObject',
    ],
    extras_require={
        'dev': [
            'pytest',
            'ipuz'
        ]
    },
    entry_points={
        'console_scripts': [
            'genxword = genxword.cli:main',
            ],
        'gui_scripts': [
            'genxword-gtk = genxword.gui:main',
            ]
        },
)
