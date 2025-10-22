# - change_dateformat_csv.py -
# Usage: python3 change_dateformat_csv.py <input_csv_file> <output_csv_file> <column_name> <dateformat_name>

import pandas as pd
import sys

dateformats = {
    'soliton': '%m/%d/%Y %H:%M:%S.%f %z', # 10/01/2024 17:02:04.161 +0900
    'squid_access': '%d/%b/%Y:%H:%M:%S %z', # 01/Oct/2024:17:04:39 +0900
    'apache_error': '%a %b %d %H:%M:%S.%f %Y %z', # Tue Oct 01 17:05:32.686430 2024 +0900
}

output_dateformat = '%Y-%m-%d %H:%M:%S.%f %z' # 2024-10-01 17:02:04.161000 +0900

# change this to the default dateformat
default_dateformat_name = 'soliton'

if len(sys.argv) > 4:
    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]
    column_name = sys.argv[3]
    dateformat_name = sys.argv[4]
    dateformat = dateformats[dateformat_name]
else:
    raise Exception("No input file or output file or column name or dateformat name specified")

df = pd.read_csv(input_csv_file)
df[column_name] = pd.to_datetime(df[column_name], format=dateformat, errors="coerce")
df[column_name] = df[column_name].dt.strftime(output_dateformat)
df.to_csv(output_csv_file, index=False)
