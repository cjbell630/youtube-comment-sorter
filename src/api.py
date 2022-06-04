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

                comment.unique_repliers = 0
                comment.most_liked_reply = 0

                if comment.is_reply:
                    comment.replies = 0
                else:
                    my_display_name = api_response.items[0].snippet.authorDisplayName
                    found_display_names = [my_display_name]

                    api_response = self.get_comments(parent_id=comment.id)
                    comment.replies = len(api_response.items)
                    if comment.replies > 0: # if there are replies to this comment
                        for reply in api_response.items: # iterate through replies
                            if reply.snippet.authorDisplayName != my_display_name: # if the reply was not made by op
                                comment.most_liked_reply = max(reply.snippet.likeCount, comment.most_liked_reply) # get the number of likes of the most liked reply
                                if reply.snippet.authorDisplayName not in found_display_names: # if a reply to this comment by this user has not been seen yet
                                    comment.unique_repliers += 1 # count them as a unique replier
                                    found_display_names.append(reply.snippet.authorDisplayName) # add their name to the list of repliers

            else:
                # print("problem occurred smh\n\n" + comment.content + "\n\n" + str(api_response) + "\n\n" + comment.id)
                inaccessible_comments += 1  # TODO use
