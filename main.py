import os
import json
from file_read import get_text
from analyzer import analyze_text

config = {
    "DOCS_FOLDER": "./documents",
    "DB_FILE": "search_index.json"
}
