from typing import List
from os.path import dirname as path_dirname, join as path_join
import re
from dataclasses import dataclass
from datetime import datetime

from src.api import YouTubeAPI
from src.parsing import read_takeout

CURRENT_DIR = path_dirname(__file__)

COMMENTS = read_takeout(path_join(CURRENT_DIR, "../res/my-comments.html"))
with open(path_join(CURRENT_DIR, "../res/API_KEY"), "r", encoding="utf-8") as file:
    API_KEY = file.read()

for comment in COMMENTS:
    print(comment.content)

api = YouTubeAPI(api_key=API_KEY)

api.get_counts(COMMENTS)
for comment in COMMENTS:
    print(comment.likes)
