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

    def close(self):
        self.db.close() 

