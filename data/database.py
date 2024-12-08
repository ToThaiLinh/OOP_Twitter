from abc import ABC, abstractmethod

class Database(ABC):
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def execute(self, query, params=None):
        pass
    
    @abstractmethod
    def fetchall(self):
        pass
    
    @abstractmethod
    def fetchone(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass
