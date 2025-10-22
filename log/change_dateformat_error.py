import sys
from pathlib import Path
from datetime import datetime
from dateutil import parser

lines = Path(sys.argv[1]).read_text().splitlines()

for line in lines:
    try:
        tokens = line.split('] ')
        date = tokens[0].strip('[]')
        others = '] '.join(tokens[1:])
        print(parser.parse(date), others)
    except:
        pass
