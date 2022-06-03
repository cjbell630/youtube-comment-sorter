from typing import List

from pyyoutube import Api
from src.parsing import Comment


class YouTubeAPI(Api):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def get_counts(self, comments: List[Comment]):
        # TODO remove
        count = 0

        for comment in comments:
            api_response = self.get_comment_thread_by_id(comment_thread_id=comment.id)
            if len(api_response.items) > 0:  # make sure successful
                comment.likes = api_response.items[0].snippet.likeCount
                # TODO reply
            else:
                print("problem occurred smh\n\n" + comment.content + "\n\n" + str(api_response) + "\n\n" + comment.id)
            if count > 50:
                return
            else:
                count += 1
                print(count)
