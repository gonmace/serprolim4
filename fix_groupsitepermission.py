"""
Fix: table "wagtailcore_groupsitepermission" already exists

Run: python fix_groupsitepermission.py

Option A: Drops the table so the migration can create it fresh.
Option B: Inserts a fake migration record (use if you're on Wagtail 7.x and
          the table was created manually or by a previous partial run).
"""
import os
import sqlite3
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='wagtailcore_groupsitepermission'"
)
if not c.fetchone():
    print("Table does not exist. No fix needed.")
    conn.close()
    exit(0)

# Option A: Drop the table (simplest - migration will recreate it)
print("Table exists. Dropping it so migration can recreate...")
c.execute("DROP TABLE wagtailcore_groupsitepermission")
conn.commit()
print("Dropped. Run: python manage.py migrate")
conn.close()
