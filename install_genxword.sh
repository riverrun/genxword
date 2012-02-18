#!/bin/bash
# Script to install genxword

read -p "Just press Enter to use the Python2.7 version. \
To use the Python3 version, press any key and then Enter."
if [[ -n $REPLY ]]; then
    sed -i '1s/python2.7/python3/' setup.py
    sed -i '1s/python2.7/python3/' genxword
    sed -i '1s/python2.7/python3/' gencrossword/gencrossword.py
    sed -i 's/raw_input/input/g' gencrossword/gencrossword.py
    sed -i 's/raw_input/input/g' gencrossword/calcxword.py
    python3 setup.py install
    APP_NAME=genxword-py3
else
    python2.7 setup.py install
    APP_NAME=genxword
fi
echo "Installing the $APP_NAME program"
cp genxword /usr/bin/$APP_NAME
chmod 755 /usr/bin/$APP_NAME

cd man
echo "Installing the man page for $APP_NAME"
cp $APP_NAME.6 /usr/share/man/man6/
gzip /usr/share/man/man6/$APP_NAME.6
