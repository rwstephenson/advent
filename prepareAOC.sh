#!/bin/bash
if [ $# -ne 2 ]; then
    echo 'Usage: prepareAOC <year> <day>'
    exit 1
fi
if [ $1 -lt 2015 ]; then
    echo 'Invalid year'
    exit 1
fi
if [ $2 -gt 25 ]; then
    echo 'Invalid day'
    exit 1
fi
cd ~/hackspace/advent/$1
mkdir dec$2
cd dec$2
cp ~/hackspace/advent/template.py dec$2.py
touch testInput.txt
