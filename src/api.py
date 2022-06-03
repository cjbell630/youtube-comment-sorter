from typing import List

from pyyoutube import Api
from src.parsing import Comment


class YouTubeAPI(Api):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def get_counts(self, comments: List[Comment]):
        inaccessible_comments = 0
        for comment in comments:
            api_response = self.get_comment_by_id(comment_id=comment.id)
            if len(api_response.items) > 0:  # make sure successful
                comment.likes = api_response.items[0].snippet.likeCount

            else:
                # print("problem occurred smh\n\n" + comment.content + "\n\n" + str(api_response) + "\n\n" + comment.id)
                inaccessible_comments += 1 # TODO use

            if comment.is_reply:
                comment.replies = 0
            else:
                api_response = self.get_comments(parent_id=comment.id)
                comment.replies = len(api_response.items)
