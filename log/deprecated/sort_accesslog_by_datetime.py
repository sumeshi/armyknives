import sys
from pathlib import Path
from datetime import datetime
# from dateutil import parser

lines = Path(sys.argv[1]).read_text().splitlines()

matrix = list()
for line in lines:
    tokens = line.split(' ')
    rawdate = ' '.join(tokens[3:5])
    matrix.append(sum([tokens[0:3], [str(datetime.strptime(rawdate, "[%d/%b/%Y:%H:%M:%S %z]").isoformat())], tokens[5:]], []))

# sortedlist = " ".join(sorted(matrix, key=lambda l: l[3]))
sortedlist = sorted(matrix, key=lambda l: l[3])
formatted_sorted_list = "\n".join(" ".join(map(str, line)) for line in sortedlist)

# Path(sys.argv[2]).write_text("\n".join(sortedlist))
Path(sys.argv[2]).write_text(formatted_sorted_list)
