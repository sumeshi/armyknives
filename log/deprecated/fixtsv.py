# coding: utf-8
from pathlib import Path
import pandas as pd
import sys

inputfile = Path(sys.argv[1])

text = inputfile.read_text()
headers = list()

buffer = ''

continueflag = False

for index, line in enumerate(text.splitlines()):
    if index == 0:
        headers = line.split('\t')
    
    if continueflag:
        buffer = buffer + line
    else:
        buffer = line

    if len(buffer.split('\t')) < len(headers):
        continueflag = True
    else:
        print(buffer)
        continueflag = False
        buffer = ''