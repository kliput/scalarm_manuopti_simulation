#!/bin/bash

IN_DIR=$1
OUT_DIR=$2

A=$3

RES=`cat $IN_DIR/res.txt`
echo "$RES $3" > $OUT_DIR/data2.txt
