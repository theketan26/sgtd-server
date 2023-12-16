from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://theketan26:ks123456@start.fbvwsga.mongodb.net/?retryWrites=true&w=majority"


class Db:
    def __init__(self):
        self.client = MongoClient(uri, server_api = ServerApi('1'))

        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client.user
        self.details_collection = self.db.details
