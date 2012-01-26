#!/bin/bash
# Script to enable you to use genxword with python3
sed -i '1s/python2.7/python3/' setup.py
sed -i '1s/python2.7/python3/' genxword
sed -i '1s/python2.7/python3/' gencrossword/gencrossword.py
sed -i 's/raw_input/input/g' gencrossword/gencrossword.py
sed -i 's/raw_input/input/g' gencrossword/calcxword.py
sed -i 's/genxword/genxword-py3/g' genxword.6
