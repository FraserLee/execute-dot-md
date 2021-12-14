#!/bin/bash

cd $(dirname $0)

./linker-dot-md/linker.py README_src.md README.md 

./execute_md.py README.md README.md 
