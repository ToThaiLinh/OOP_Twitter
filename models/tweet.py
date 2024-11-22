class Tweet:
    def __init__(self, tweet_id, content, created_at, media, comment_cnt, repost_cnt, like_cnt, view_cnt):
        self.tweet_id = tweet_id
        self.content = content
        self.created_at = created_at
        self.media = media
        self.comment_cnt = comment_cnt
        self.repost_cnt = repost_cnt
        self.like_cnt = like_cnt
        self.view_cnt = view_cnt