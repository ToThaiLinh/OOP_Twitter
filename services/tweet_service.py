class TweetService:
    def __init__(self, db):
        self.db = db
        self.db.connect() 
    
    def create(self, tweet_id, created_at, content, media, comment_cnt, repost_cnt, like_cnt, view_cnt):
        try:
            query = """
            INSERT INTO tweets (tweet_id, created_at, content, media, comment_cnt, repost_cnt, like_cnt, view_cnt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            created_at = VALUES(created_at),
            content = VALUES(content),
            media = VALUES(media),
            comment_cnt = VALUES(comment_cnt),
            repost_cnt = VALUES(repost_cnt),
            like_cnt = VALUES(like_cnt),
            view_cnt = VALUES(view_cnt)
            """
            params = (tweet_id, created_at, content, media, comment_cnt, repost_cnt, like_cnt, view_cnt)
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:

            print(f"Error occurred while inserting user: {e}")
            self.db.rollback() 

    def create_multiple(self, tweets):
        query = "INSERT INTO tweets (tweet_id, created_at, content, media, comment_cnt, repost_cnt, like_cnt, view_cnt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = [(tweet["tweet_id"], tweet["created_at"], tweet["content"], tweet["media"], tweet["comment_cnt"], tweet["repost_cnt"], tweet["like_cnt"], tweet["view_cnt"]) for tweet in tweets]
        self.db.execute_many(query, params) 
        self.db.commit()

    def save_hashtag(self, hashtag_name):
        query = """
        INSERT IGNORE INTO hashtags (hashtag_name)
        VALUES (%s)
        """
        try:
            self.db.execute(query, (hashtag_name,))
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting hashtag: {e}")
            self.db.rollback() 
    
    def save_have_hashtag(self, hashtag_name, tweet_id):
        query = """
        INSERT IGNORE INTO tweet_have_hashtags (hashtag_name, tweet_id)
        VALUES (%s, %s)
        """
        params = (hashtag_name, tweet_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting have_hashtag: {e}")
            self.db.rollback() 
    

    def close(self):
        self.db.close() 


