#!/bin/bash
# Script to install genxword, which depends on Python (2.7 or 3) and Pycairo.
# This script does not check for dependencies. That's your job.

set -e
ERROR_MESSAGE="$(tput bold)$(tput setaf 1)An error occurred. \
Please read the output above to see what the problem is.$(tput sgr0)"
MAN_DIR=/usr/share/man/man6

echo -e "Just press Enter to use the Python 2.7 version.\n\
To use the Python 3 version, press any key and then Enter."
read PYVERSION
if [[ -n $PYVERSION ]]; then
    python3 setup.py install || { echo -e $ERROR_MESSAGE; exit 1; }
    APP_NAME=genxword-py3
else
    python2.7 setup.py install || { echo -e $ERROR_MESSAGE; exit 1; }
    APP_NAME=genxword
fi
echo "Installing the $APP_NAME program"
cp $APP_NAME /usr/bin/ && chmod 755 /usr/bin/$APP_NAME || { echo -e $ERROR_MESSAGE; exit 1; }

cd man
echo "Installing the man page for $APP_NAME"
cp $APP_NAME.6 $MAN_DIR && gzip $MAN_DIR/$APP_NAME.6 || { echo -e $ERROR_MESSAGE; exit 1; }

echo -e "$(tput bold)$(tput setaf 2)The program $APP_NAME has been successfully installed.\n\
Run $APP_NAME -h for basic info about the program or read the man page for further options.$(tput sgr0)"
