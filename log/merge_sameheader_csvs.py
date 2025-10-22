#!/usr/bin/env python3
# merge_sameheader_csvs.py
# usage: python merge_sameheader_csvs.py file1.csv file2.csv ... output.csv

import sys
import pandas as pd
from pathlib import Path

if len(sys.argv) < 4:
    print("[ERROR] Usage: python merge_sameheader_csvs.py file1.csv file2.csv ... output.csv")
    sys.exit(1)

input_files = sys.argv[1:-1]
output_file = sys.argv[-1]

dfs = []
header_ref = None
header_mismatch = False

for f in input_files:
    path = Path(f)
    if not path.exists():
        print(f"[ERROR] File not found: {f}")
        continue

    try:
        df = pd.read_csv(f, dtype=str)
    except Exception as e:
        print(f"[ERROR] Failed to read {f}: {e}")
        continue

    header = list(df.columns)

    if header_ref is None:
        header_ref = header
        ref_name = f
    else:
        if header != header_ref:
            header_mismatch = True
            print(f"[ERROR] Header mismatch: {f}")
            max_len = max(len(header_ref), len(header))
            for i in range(max_len):
                h1 = header_ref[i] if i < len(header_ref) else "(none)"
                h2 = header[i] if i < len(header) else "(none)"
                if h1 != h2:
                    print(f"[ERROR] Column {i+1}: '{h1}' ≠ '{h2}'")

    dfs.append(df)

if not dfs:
    print("[ERROR] No valid CSVs found.")
    sys.exit(1)

merged = pd.concat(dfs, ignore_index=True)

merged.to_csv(output_file, index=False, encoding="utf-8")

if header_mismatch:
    print("[ERROR] Some CSV headers are mismatched.")
else:
    print("[INFO] All CSV headers are matched.")

print(f"[INFO] Merged result saved to {output_file}.")
