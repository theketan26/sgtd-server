from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId


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
        self.creds_collection = self.db.credentials


    def get_user(self, number, detail = False):
        if detail:
            document = self.details_collection.find_one({"number": number})
        else:
            document = self.creds_collection.find_one({"number": number})
        return document


    def add_user(self, user_data):
        report = {
            'status': False,
            'message': None
        }

        result = self.get_user(user_data['number'])

        if result:
            report['message'] = 'User already exist'
            return report

        result = self.creds_collection.insert_one(user_data)

        try:
            report['status'] = True
            report['message'] = str(result.inserted_id)
            print(f"User added with ID: {result.inserted_id}")
            user_data.pop('password')
            user_data.update({
                'name': None,
                'email': None,
                'position': 1
            })
            self.add_user_details(user_data)
        except Exception as e:
            report['status'] = False
            report['message'] = f"Error occurred as {e}"
            print(f"Error occurred as {e}")

        return report


    def add_user_details(self, user_data):
        report = {
            'status': False,
            'message': None
        }

        result = self.get_user(user_data['number'], True)

        if result:
            report['message'] = 'User already exist'
            return report

        if not 6000000000 < user_data['number'] < 9999999999:
            report['message'] = 'Mobile number invalid'
            return report

        if not 0 < user_data['position'] < 5:
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


    def delete_user(self, number):
        try:
            result = self.creds_collection.delete_one({"number": int(number)})
            result = self.details_collection.delete_one({"number": int(number)})

            if result.deleted_count > 0:
                print(f"Document with number {number} deleted successfully.")
                return True
            else:
                print(f"No document found with number {number}.")
                return False

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


    def update_user(self, user_data):
        try:
            result = self.details_collection.update_one({"number": user_data.number}, {"$set": {
                'number': user_data.number,
                'name': user_data.name,
                'email': user_data.email,
                'position': user_data.position
            }})

            if result.modified_count > 0:
                print(f"User data for user with number {user_data.number} updated successfully.")
                return True
            else:
                print(f"No user found with number {user_data.number}. Nothing to update.")
                return False

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


    def update_password(self, user_data):
        try:
            result = self.creds_collection.update_one({"number": user_data.number}, {"$set": {
                'number': user_data.number,
                'password': user_data.password
            }})

            if result.modified_count > 0:
                print(f"User data for user with number {user_data.number} updated successfully.")
                return True
            else:
                print(f"No user found with number {user_data.number}. Nothing to update.")
                return False

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
