#!/bin/sh

truncate -s 0 out.txt
date >> out.txt
python3 arc_consistency.py >> out.txt