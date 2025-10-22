import sys
from pathlib import Path
from datetime import datetime
from dateutil import parser

lines = Path(sys.argv[1]).read_text().splitlines()

for line in lines:
    tokens = line.split(' ')
    rawdate = ' '.join(tokens[3:5])
    date = rawdate.strip('[]')
    date = date.replace(':', ' ', 1)
    others1 = ' '.join(tokens[0:3])
    others2 = ' '.join(tokens[5:])
    print(parser.parse(date), others1, others2)
        
