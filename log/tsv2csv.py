import pandas as pd
import sys

""" tsv2csv.py - convert tsv to csv
Usage: python3 tsv2csv.py <input_tsv_file> <output_csv_file>
"""

def tsv_to_csv(input_tsv_file, output_csv_file):
    try:
        df = pd.read_csv(input_tsv_file, sep='\t', encoding='utf-8', quoting=1)
    except UnicodeDecodeError:
        df = pd.read_csv(input_tsv_file, sep='\t', encoding='shift_jis', quoting=1)

    df.to_csv(output_csv_file, index=False)

if __name__ == "__main__":
    tsv_to_csv(sys.argv[1], sys.argv[2])
