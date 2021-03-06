import re
from dataclasses import dataclass
from datetime import datetime
from typing import List
from json import loads as json_loads

from src.util import replace_html_escapes, dict_to_json_string


@dataclass
class Comment:
    id: str
    video_id: str
    likes: int
    replies: int
    unique_repliers: int
    most_liked_reply: int
    date_posted: datetime
    content: str
    is_reply: bool = False

    def __str__(self):
        return f"https://www.youtube.com/watch?v={self.video_id}&lc={self.id}\n" \
               f"◢◣  {self.date_posted.astimezone().strftime('%c')}\n" \
               f"◥◤      {self.content}\n" \
               f"    👍{self.likes:8}      👎    Replies: {self.replies}"


COMMENTS: List[Comment] = []
REGEX = {
    # video id, comment id, date string (YYYY-MM-DD HH:MM:SS UTC), Comment content
    "REPLY": r"You <a href=\"http:\/\/www\.youtube\.com\/watch\?v=(.*?)&amp;lc=(.*?)\">.*?a video<\/a> at (.*?).<br\/>((.|\n)*?)<\/li>",
    # video id, comment id, date string (YYYY-MM-DD HH:MM:SS UTC), Comment content
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
                    -1, -1, -1, -1,
                    datetime.strptime(regex_data[2], "%Y-%m-%d %H:%M:%S %Z"),
                    content=replace_html_escapes(regex_data[3]),
                    is_reply=is_reply
                ))
        return comments


def save_backup(comments: List[Comment], complete_path: str):
    json = []
    for comment in comments:
        json.append({
            "id": comment.id,
            "video_id": comment.video_id,
            "likes": comment.likes,
            "replies": comment.replies,
            "unique_repliers": comment.unique_repliers,
            "most_liked_reply": comment.most_liked_reply,
            "date_posted": comment.date_posted.timestamp(),
            "content": comment.content,
            "is_reply": comment.is_reply
        })
    with open(complete_path, "w", encoding="utf-8") as file:
        file.write(dict_to_json_string(json))


def load_backup(complete_path: str) -> List[Comment]:
    comments: List[Comment] = []
    with open(complete_path, "r", encoding="utf-8") as file:
        json = json_loads(file.read())
    for comment_json in json:
        comments.append(
            Comment(
                id=comment_json["id"],
                video_id=comment_json["video_id"],
                likes=comment_json["likes"],
                replies=comment_json["replies"],
                unique_repliers=comment_json["unique_repliers"],
                most_liked_reply=comment_json["most_liked_reply"],
                date_posted=datetime.utcfromtimestamp(comment_json["date_posted"]),
                content=comment_json["content"],
                is_reply=comment_json["is_reply"]
            )
        )
    return comments
