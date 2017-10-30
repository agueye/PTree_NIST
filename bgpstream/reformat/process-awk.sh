#!/bin/bash

gunzip -dc 2015.allpaths.gz | time awk -f proc.awk | gzip -1 > 2015.allpaths-awk.gz
# 1245.76user 14.22system 21:01.11elapsed 99%CPU (0avgtext+0avgdata 1196maxresident)k
