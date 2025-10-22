import sys
from pathlib import Path
from datetime import datetime
from dateutil import parser

lines = Path(sys.argv[1]).read_text().splitlines()
outfile = Path(sys.argv[2])

with outfile.open("a", encoding="utf-8") as f:
  for line in lines:
      tokens = line.split(' ')
      rawdate = ' '.join(tokens[3:5])
      date = rawdate.strip('[]')
      date = date.replace(':', ' ', 1)
      others1 = ' '.join(tokens[0:3])
      others2 = ' '.join(tokens[5:])
      try:
        f.write(f"{parser.parse(date)}, {others1}, {others2}\n")
      except:
        print("ERROR: ", line)
