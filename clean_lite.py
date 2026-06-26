#!/usr/bin/env python3
"""Data Cleaner — Free Lite Edition. Auto-detect and fix messy CSV data."""
import csv, sys, re
from collections import Counter

def clean_csv(filepath):
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader, [])
        rows = list(reader)
    
    print(f"Data Cleaner Lite — {filepath}")
    print(f"Rows: {len(rows)} | Cols: {len(headers)}")
    issues = 0
    
    for i, col in enumerate(headers):
        vals = [r[i] if i < len(r) else '' for r in rows]
        empty = sum(1 for v in vals if not v.strip())
        if empty: 
            print(f"  [{col}] {empty} empty cells")
            issues += empty
    
    # Detect duplicates
    seen = set()
    dupes = 0
    for row in rows:
        key = '|'.join(str(c).strip().lower() for c in row)
        if key in seen: dupes += 1
        else: seen.add(key)
    if dupes: print(f"  {dupes} duplicate rows found")
    
    print(f"Total issues: {issues + dupes}")
    if issues + dupes == 0:
        print("Data looks clean!")
    print(f"\nNeed auto-fix? Full Data Cleaner: https://payhip.com/DataCrafted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 clean_lite.py data.csv")
        sys.exit(0)
    clean_csv(sys.argv[1])
