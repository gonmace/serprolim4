"""
Fix: index "referenceindex_source_object" already exists

Run: python fix_referenceindex_index.py

Drops the indexes so the migration can recreate them (Wagtail 7.2.1+).
"""
import os
import sqlite3

os.chdir(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

INDEXES = ['referenceindex_source_object', 'referenceindex_target_object']

for index_name in INDEXES:
    c.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name=?",
        (index_name,)
    )
    if not c.fetchone():
        print(f"Index {index_name} does not exist, skip.")
        continue
    try:
        c.execute(f'DROP INDEX IF EXISTS {index_name}')
        conn.commit()
        print(f"Dropped index: {index_name}")
    except Exception as e:
        print(f"Error dropping {index_name}: {e}")

conn.close()
print("Done. Run: python manage.py migrate")
