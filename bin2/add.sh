#!/bin/bash

A=`cat data2.txt | cut -d ' ' -f1`
B=`cat data2.txt | cut -d ' ' -f2`

echo $A
echo $B

expr $A \+ $B > res2.txt
