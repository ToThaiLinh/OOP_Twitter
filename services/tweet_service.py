class TweetService:
    def __init__(self, db):
        self.db = db
        self.db.connect() 
    
    def create(self, tweet_id, created_at, content, media, comment_cnt, repost_cnt, like_cnt, view_cnt):
        try:
            query = "INSERT INTO tweets (tweet_id, created_at, content,  media, comment_cnt, repost_cnt, like_cnt, view_cnt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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

    def save_hashtag(self, hashtag_id, hashtag_name):
        query = """
        INSERT INTO hashtags (hashtag_id, hashtag_name)
        VALUES (%s, %s)
        """
        params = (hashtag_id, hashtag_name)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting hashtag: {e}")
            self.db.rollback() 
    
    def save_have_hashtag(self, have_hashtag_id, hashtag_id, tweet_id):
        query = """
        INSERT INTO tweet_have_hashtags (have_hashtag_id, hashtag_id, tweet_id)
        VALUES (%s, %s, %s)
        """
        params = (have_hashtag_id, hashtag_id, tweet_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting have_hashtag: {e}")
            self.db.rollback() 
    

    def close(self):
        self.db.close() 


