import re
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.util import replace_html_escapes


@dataclass
class Comment:
    id: str
    video_id: str
    likes: int
    replies: int
    date_posted: datetime
    content:str
    is_reply: bool = False


COMMENTS: List[Comment] = []
REGEX = {
    #video id, comment id, date string (YYYY-MM-DD HH:MM:SS UTC), Comment content
    "REPLY": r"You <a href=\"http:\/\/www\.youtube\.com\/watch\?v=(.*?)&amp;lc=(.*?)\">.*?a video<\/a> at (.*?).<br\/>((.|\n)*?)<\/li>",
    #video id, comment id, date string (YYYY-MM-DD HH:MM:SS UTC), Comment content
    "COMMENT": r"You added a <a href=\"http:\/\/www\.youtube\.com\/watch\?v=(.*?)&amp;lc=(.*?)\">.*?a video<\/a> at (.*?).<br\/>((.|\n)*?)<\/li>"
}


def read_takeout(complete_path: str) -> List[Comment]:
    comments: List[Comment] = []
    with open(complete_path, "r", encoding="utf-8") as file:
        raw = file.read()
        for line in raw.split("<li>"):
            regex_data = re.findall(REGEX["REPLY"], line)
            is_reply = True
            if len(regex_data) == 0:
                is_reply = False
                regex_data = re.findall(REGEX["COMMENT"], line)
            # video id, comment id, date string (YYYY-MM-DD HH:MM:SS UTC), Comment content
            if len(regex_data) == 0:
                print("post: \n\n\n" + line + "\n\n\n\n")
            else:
                regex_data = regex_data[0]
                comments.append(Comment(
                    regex_data[1],
                    regex_data[0],
                    -1, -1,
                    datetime.strptime(regex_data[2], "%Y-%m-%d %H:%M:%S %Z"),
                    content=replace_html_escapes(regex_data[3]),
                    is_reply=is_reply
                ))
        return comments