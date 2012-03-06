#!/bin/sh
# Script to convert a dictionary file into a file that can be used with genxword
# This script will produce a file with words 3-11 words long, delete any non-alphabetic
# characters, and if there are any clues, it will print them as well.

awk '{
if ($1 ~ "^[[:alpha:]]+$" && a[tolower($1)]++ == 0 && length($1) > 2 && length($1) < 12)
    print $0;
}' "$@" > "$@".new
