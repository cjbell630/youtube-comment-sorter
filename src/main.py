from os.path import dirname as path_dirname, join as path_join, exists

from src.api import YouTubeAPI
from src.parsing import read_takeout, save_backup, load_backup

CURRENT_DIR = path_dirname(__file__)
BACKUP_PATH = path_join(CURRENT_DIR, "../res/backup.json")

SORTING_METHODS = {
    "LIKES": lambda c: c.likes,
    "REPLIES": lambda c: c.replies,
    "UNIQUE REPLIERS": lambda c: c.replies,
    "DATE": lambda c: c.date_posted.timestamp(),
    "LIKES TO REPLIES RATIO": lambda c: c.replies / c.likes if c.likes > 0 and c.replies > 0 else 0,
    "LIKES TO UNIQUE REPLIERS RATIO": lambda c: c.unique_repliers / c.likes if c.likes > 0 and c.unique_repliers > 0 else 0,
    #"LIKES TO MOST LIKED REPLY RATIO": lambda c: c.most_liked_reply / c.likes if c.likes > 0 and c.most_liked_reply > 0 else 0
    "LIKES TO MOST LIKED REPLY RATIO": lambda c: c.most_liked_reply - c.likes
}

with open(path_join(CURRENT_DIR, "../res/API_KEY"), "r", encoding="utf-8") as file:
    API_KEY = file.read()

if __name__ == "__main__":

    if exists(BACKUP_PATH):
        print("> found backup, loading...")
        COMMENTS = load_backup(BACKUP_PATH)
    else:
        print("> no backup found, reading takeout file...")
        COMMENTS = read_takeout(path_join(CURRENT_DIR, "../res/my-comments.html"))
        api = YouTubeAPI(api_key=API_KEY)

        print("> contacting api for like and reply counts... please be patient, this may take a while...")
        api.get_counts(COMMENTS)

        print("> saving backup...")
        save_backup(COMMENTS, BACKUP_PATH)

    print("> sorting...")
    COMMENTS.sort(key=SORTING_METHODS["LIKES TO MOST LIKED REPLY RATIO"], reverse=True)

    for comment in COMMENTS:
        print(str(comment) + "\n\n")
