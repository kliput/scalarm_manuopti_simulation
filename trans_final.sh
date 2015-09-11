#!/bin/bash

IN_DIR=$1

RES=`cat $IN_DIR/res2.txt`

echo "trans final"

echo "final_res $RES" > final_results.txt
