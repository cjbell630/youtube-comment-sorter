from typing import List
from os.path import dirname as path_dirname, join as path_join, exists
import re
from dataclasses import dataclass
from datetime import datetime

from src.api import YouTubeAPI
from src.parsing import read_takeout, save_backup, load_backup

CURRENT_DIR = path_dirname(__file__)
BACKUP_PATH = path_join(CURRENT_DIR, "../res/backup.json")

with open(path_join(CURRENT_DIR, "../res/API_KEY"), "r", encoding="utf-8") as file:
    API_KEY = file.read()

if __name__ == "__main__":

    if exists(BACKUP_PATH):
        COMMENTS = load_backup(BACKUP_PATH)
    else:
        COMMENTS = read_takeout(path_join(CURRENT_DIR, "../res/my-comments.html"))
        api = YouTubeAPI(api_key=API_KEY)

        api.get_counts(COMMENTS)
        for comment in COMMENTS:
            print(comment.likes)
        save_backup(COMMENTS[:50], BACKUP_PATH)

    for comment in COMMENTS:
        print(comment.content)
