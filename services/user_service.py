class UserService:
    def __init__(self, db):
        self.db = db
        self.db.connect() 
    
    def create(self, user_id, username, role, joined_at, following, follower, posts_cnt):
        try:
            query = """
            INSERT INTO users (user_id, username, role, joined_at, following, follower, posts_cnt) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
                username = VALUES(username),
                role = VALUES(role),
                joined_at = VALUES(joined_at),
                following = VALUES(following),
                follower = VALUES(follower),
                posts_cnt = VALUES(posts_cnt)
            """
            params = (user_id, username, role, joined_at, following, follower, posts_cnt)
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:

            print(f"Error occurred while inserting user: {e}")
            self.db.rollback() 

    def create_multiple(self, users):
        query = "INSERT INTO users (user_id, username, role, joined_at, following, follower, posts_cnt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = [(user["user_id"], user["username"], user["role"], user["joined_at"], user["following"], user["follower"], user["posts_cnt"]) for user in users]
        self.db.execute_many(query, params) 
        self.db.commit()
    
    def save_follower(self, user_id, follower_user_id) :
        query = """
        INSERT IGNORE INTO followers (user_id, follower_user_id)
        VALUES (%s, %s)
        """
        params = (user_id, follower_user_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting follower: {e}")
            self.db.rollback() 
    
    def save_following(self, user_id, following_user_id) :
        query = """
        INSERT IGNORE INTO followings (user_id, following_user_id)
        VALUES (%s, %s)
        """
        params = (user_id, following_user_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting following: {e}")
            self.db.rollback() 
    def save_mention(self, user_id, tweet_id):
        query = """
        INSERT IGNORE INTO mentions (user_id, tweet_id)
        VALUES (%s, %s)
        """
        params = (user_id, tweet_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting mention: {e}")
            self.db.rollback() 
    def save_post_tweet(self, user_id, tweet_id):
        query = """
        INSERT IGNORE INTO user_post_tweet (user_id, tweet_id)
        VALUES (%s, %s)
        """
        params = (user_id, tweet_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting post_tweet: {e}")
            self.db.rollback() 
    
    def save_comment_tweet(self, user_id, tweet_id):
        query = """
        INSERT IGNORE INTO user_comment_tweet (user_id, tweet_id)
        VALUES (%s, %s)
        """
        params = (user_id, tweet_id)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting comment_tweet: {e}")
            self.db.rollback() 
    def save_repost(self, user_id, tweet_id, type, content):
        query = """
        INSERT INTO reposts (user_id, tweet_id, type, content)
        VALUES ( %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        type = VALUES(type), content = VALUES(content)
        """
        params = (user_id, tweet_id, type, content)
        try:
            self.db.execute(query, params)
            self.db.commit()
        except Exception as e:
            print(f"Error occurred while inserting reposts: {e}")
            self.db.rollback() 

    def close(self):
        self.db.close() 
