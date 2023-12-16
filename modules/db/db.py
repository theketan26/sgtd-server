from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://theketan26:ks123456@start.fbvwsga.mongodb.net/?retryWrites=true&w=majority"


class Db:
    def __init__(self):
        self.client = MongoClient(uri, server_api = ServerApi('1'))

        try:
            print("Starting to ping!")
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client.user
        self.details_collection = self.db.details


    def add_user(self, user_data):
        report = {
            'status': False,
            'message': None
        }

        if not 6000000000 < user_data['mobile'] < 9999999999:
            report['message'] = 'Mobile number invalid'
            return report

        if not 0 < user_data['type'] < 5:
            report['message'] = 'Type invalid'
            return report

        result = self.details_collection.insert_one(user_data)

        try:
            report['status'] = True
            report['message'] = str(result.inserted_id)
            print(f"User added with ID: {result.inserted_id}")
        except Exception as e:
            report['status'] = False
            report['message'] = f"Error occurred as {e}"
            print(f"Error occurred as {e}")

        return report
