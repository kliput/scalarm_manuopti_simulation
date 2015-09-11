#!/bin/bash

# $1 - input file path
# input file: "A B"

if [ "$1" == "" ]; then
  echo "usage: ./program <file_path>"
  exit 1
fi

A=`cat data.txt | cut -d ' ' -f1`
B=`cat data.txt | cut -d ' ' -f2`

echo $A
echo $B

expr $A \* $B > res.txt
