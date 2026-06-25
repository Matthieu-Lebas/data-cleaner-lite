#!/usr/bin/env python3
"""Data Cleaner Toolkit — Auto-detect and fix messy data."""
import sys, csv, re, os

def clean_csv(input_path, output_path=None):
    with open(input_path) as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    report = {"rows": len(rows), "cols": len(headers), "issues_fixed": 0}
    
    for col_idx, header in enumerate(headers):
        values = [r[col_idx] if col_idx < len(r) else "" for r in rows]
        non_empty = [v for v in values if v.strip()]
        
        numeric = 0
        for v in non_empty[:100]:
            try:
                float(v.replace(",","").replace("$","").replace("%",""))
                numeric += 1
            except:
                pass
        is_numeric = numeric / max(len(non_empty[:100]), 1) > 0.8
        
        for row_idx, row in enumerate(rows):
            if col_idx >= len(row):
                row.append("")
                report["issues_fixed"] += 1
            val = row[col_idx]
            if is_numeric and val:
                val = val.strip().replace("$","").replace("\u20ac","").replace("%","")
                val = val.replace(",", "") if val.count(",") <= 1 else val
                cleaned = re.sub(r"[^0-9.\-]", "", val)
                if cleaned and cleaned.count(".") <= 1:
                    try:
                        float(cleaned)
                        val = cleaned
                    except:
                        pass
            else:
                val = val.strip()
            if val != row[col_idx]:
                row[col_idx] = val
                report["issues_fixed"] += 1
    
    out = output_path or input_path.replace(".csv", "_clean.csv")
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    
    print(f"Data Cleaner Report")
    print(f"  Rows: {report['rows']} | Columns: {report['cols']}")
    print(f"  Issues fixed: {report['issues_fixed']}")
    print(f"  Output: {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Data Cleaner Toolkit\n  python3 clean.py messy_data.csv")
        sys.exit(0)
    clean_csv(sys.argv[1])
