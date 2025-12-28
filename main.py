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

def remove_file_from_db(current_paths):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT path FROM documents")
    db_paths = set()
    for row in c.fetchall():
        path = row[0]
        db_paths.add(path)
    current_paths_set = set(current_paths)
    delete = current_paths_set - db_paths
    for path in delete:
        c.execute("DELETE FROM documents WHERE path = ?",(path,))
    conn.commit()
    conn.close()
    
def run_indexing():
    if not os.path.exists(DOCS_FOLDER):
        os.makedirs(DOCS_FOLDER)
    init_db()

    all_file_paths = []
    for root, dirs, files in os.walk(DOCS_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            all_file_paths.append(file_path)

    remove_file_from_db(all_file_paths)

    for file_path in all_file_paths:
        file_name = os.path.basename(file_path)
        last_modified = get_time_modified(file_path)
        current_modified_time = os.path.getmtime(file_path)
        if current_modified_time == last_modified:
            continue
        text = get_text(file_path)
        if not text:
            continue
        analysis = analyze_text(text)
        add_file_to_db(file_name,file_path,current_modified_time,analysis)
