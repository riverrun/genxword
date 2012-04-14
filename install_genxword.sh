#!/bin/sh
# Script to install genxword, which depends on Python (2.7 or 3) and Pycairo.

ERROR_MESSAGE="$(tput bold)$(tput setaf 1)An error occurred. \
Please read the output above to see what the problem is.$(tput sgr0)\n"
MAN_DIR=/usr/share/man/man1

printf "Just press Enter to use the Python 2.7 version.\n\
To use the Python 3 version, press any key and then Enter.\n"
read PYVERSION
if [ -z $PYVERSION ]; then
    python2.7 setup.py install || { printf "$ERROR_MESSAGE"; exit 1; }
    APP_NAME=genxword
else
    python3 setup.py install || { printf "$ERROR_MESSAGE"; exit 1; }
    APP_NAME=genxword3
fi

cd man
printf "Installing the man page for $APP_NAME\n"
cp $APP_NAME.1 $MAN_DIR && gzip -f $MAN_DIR/$APP_NAME.1 || { printf "$ERROR_MESSAGE"; exit 1; }

printf "$(tput setaf 2)The program $APP_NAME has been successfully installed.\n\
Run $APP_NAME -h for basic info about the program or read the man page for further options.$(tput sgr0)\n"
