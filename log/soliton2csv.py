import csv
import re
import sys
import codecs

# - soliton2csv.py -
# fork from https://github.com/N4SOC/fortilogcsv
#
# Usage: python3 soliton2csv {LOGFILE} {OUTPUTFILE}
#        LogFormat: "10/14/2022 16:45:00.261 +0900 loc=en-US type=ITM2 ..."
#
# Note:
# - The tool will generate a csv file with the same name as the log file, but with a .csv extension.
# - The csv files converted by this tool are not sorted by timestamp.

if len(sys.argv) > 2:
    inputfile = str(sys.argv[1])
    outputfile = str(sys.argv[2])
else:
    raise Exception("No input file or output file specified")

# Open log file for read if exists
print("[+] Reading logs from " + inputfile)
try:
    log_data = codecs.open(inputfile, "r", encoding="UTF-8")
except:
    raise Exception("Invalid input file")
# Regex matches "field=value" or "field=""more words""" syntax
# pattern = re.compile('(\w+)(?:=)(?:"{1,3}([\w\-\.:\ =]+)"{1,3})|(\w+)=(?:([\w\-\.:\=]+))')
pattern = re.compile(r'(\w+)(?:=)(?:"{1,3}([^\n"]+?)"{1,3})|(\w+)=(?:([^\s]+))')
events = []

for line in log_data:
    logline = f'timestamp="{line}'.replace('+0900', '+0900"')
    event = {}
    match = pattern.findall(logline)  # Find all regex matches on each line
    for group in match:
        # add a key,value pair to the dict for each key=value group
        if group[0] != "":
            event[group[0]] = group[1]
        else:
            event[group[2]] = group[3]
    events.append(event)

print("[+] Processing log fields")
headers = []
for row in events:
    for key in row.keys():
        if not key in headers:
            headers.append(key)

print("[+] Writing CSV")
#Added the newline option to prevent blank rows from outputting to CSV
with open(outputfile, 'w', newline='', encoding='utf-8') as fileh:
    csvfile = csv.DictWriter(fileh, headers)  # Write headers
    csvfile.writeheader()
    for row in events:
        csvfile.writerow(row)
print("[+] Finished - " + str(len(events)) + " rows written to " + outputfile)