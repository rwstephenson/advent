#!/bin/bash
if [ $# -ne 3 ]; then
    echo 'Usage: prepareAOC <year> <day> <session>'
    echo "Get session by inspecting AOC, network, headers, cookie.  Export into variable"
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
curl https://adventofcode.com/$1/day/$2/input --cookie "session=$3" > input.txt
