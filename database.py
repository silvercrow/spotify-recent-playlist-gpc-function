
import pymongo


class MongoDBConnection:
    def __init__(self, connection_string, database_name):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.connection_string)
            db = self.client[self.database_name]
            print("Connected to MongoDB successfully!")
            return db
        except pymongo.errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from MongoDB")