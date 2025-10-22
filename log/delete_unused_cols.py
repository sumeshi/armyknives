#!/usr/bin/env python3
# delete_unused_cols.py
# usage: python delete_unused_cols.py input.csv output.csv col1,col2,col3

import sys
import pandas as pd

if len(sys.argv) > 1:
    input_csv_file = sys.argv[1]
    output_csv_file = sys.argv[2]
    cols_to_drop = sys.argv[3].split(",")
else:
    raise Exception("No input file or output file or columns to drop specified")

df = pd.read_csv(input_csv_file)

df = df.drop(columns=cols_to_drop, errors="ignore")
df.to_csv(output_csv_file, index=False)