import sqlite3
import json
import os
import sys

# Set UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conn = sqlite3.connect(r'C:\Users\HYY\AppData\Roaming\WorkBuddy\automations\automations.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables:", [t[0] for t in tables])

for table in tables:
    tname = table[0]
    cur.execute(f"PRAGMA table_info({tname})")
    cols = cur.fetchall()
    print(f"\n=== {tname} columns ===")
    for col in cols:
        print(f"  {col[1]} ({col[2]})")
    cur.execute(f"SELECT * FROM {tname}")
    rows = cur.fetchall()
    print(f"\n=== {tname} rows ({len(rows)}) ===")
    for row in rows:
        row_str = str(row)
        safe = row_str.encode('utf-8', errors='replace').decode('utf-8')
        if 'seo' in safe.lower() or 'gongkao' in safe.lower() or 'autopub' in safe.lower() or 'publish' in safe.lower() or 'article' in safe.lower() or 'cron' in safe.lower() or '06' in safe or 'rrule' in safe.lower():
            print(f"  MATCH: {safe[:300]}")
        else:
            print(f"  {safe[:200]}")
conn.close()
