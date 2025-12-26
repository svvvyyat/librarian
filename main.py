import os
import json
import sqlite3
from file_read import get_text
from analyzer import analyze_text

DOCS_FOLDER = "documents"
DB_FILE = "search_index.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            path TEXT UNIQUE,
            date_modified REAL,
            description TEXT,
            keywords TEXT)''')
    conn.commit()
    conn.close()

def add_file_to_db(filename,path,time_modified,analysis):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    descriptioon = analysis.get("description","")
    keywords = json.dumps(analysis.get("keywords",[]))
    c.execute("INSERT OR REPLACE INTO documents VALUES (?,?,?,?,?,?)",(filename,path,time_modified,descriptioon,keywords))
    conn.commit()
    conn.close()

def get_time_modified(path):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date_modified FROM documents WHERE path = ?",(path,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

