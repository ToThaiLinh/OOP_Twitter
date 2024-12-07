class UserService:
    def __init__(self, db):
        self.db = db
        self.db.connect() 
    
    def create(self, user_id):
        query = "INSERT INTO users (user_id) VALUES (%s)"
        params = (user_id,)
        self.db.execute(query, params)
        self.db.commit()


    def close(self):
        self.db.close()
