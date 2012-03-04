#!/bin/sh
# Script to convert a dictionary file into a file that can be used with genxword

awk 'length($1) > 2 && length($1) < 12' $1 > $1_new.txt
