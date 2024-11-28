from pymongo import MongoClient
from database import Database

class MongoDBDatabase(Database):
    def __init__(self, uri, database):
        self.uri = uri
        self.database = database
        self.client = None
        self.db = None
    
    def connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.database]

    def execute(self, query, params=None):
        pass

    def fetchall(self):
        return list(self.db.users.find()) 

    def fetchone(self):
        return self.db.users.find_one() 
    
    def close(self):
        self.client.close()
