import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
import json
from dotenv import load_dotenv
import re


load_dotenv()


URI = os.getenv('MONGO_URI')
CRYPTO_KEY = os.getenv("CRYPTO_KEY")


class Db:
    def __init__(self):
        self.client = MongoClient(URI, server_api = ServerApi('1'))

        try:
            print("Starting to ping!")
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = self.client.user
        self.event = self.client.event
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

        fernet = Fernet(CRYPTO_KEY)
        user_data['password'] = fernet.encrypt(bytes(user_data['password'], 'utf-8'))
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


    def get_event_on_date(self, date):
        y, m, d  = date.split('-')
        try:
            # result = eval(f'self.db._{y}.find_one({{"date": f"{m}-{d}"}})')
            s = f'{m}'
            st = f'{m}-{d}'
            sti = ''
            # result = st
            result = self.event.get_collection(y).find_one({"date": st})
            # result = self.event.get_collection(y).find({"date": {"$regex": st}})
            if result == None:
                return {
                    "status": False,
                    "message": f"No event found on {st}"
                }

            result.pop('_id')

            events = result['event_id']
            result = []

            for event in events:
                res = self.event.get_collection(f"{y}_data").find_one({"event_id": event})
                res.pop('_id')
                res = {
                    'event_id': res['event_id'],
                    'title': res['desc']['title'],
                    'host': res['desc']['host']['name'],
                    'booker_name': res['desc']['booker']['name'],
                    'booker_number': res['desc']['booker']['number']
                }
                result.append(res)

            return {
                "status": True,
                "data": result,
            }

        except Exception as e:
            return {
                "status": False,
                "message": f"An unexpected error occurred: {e}"
            }


    def get_event_on_id(self, date, id):
        y, m, d  = date.split('-')
        try:
            res = self.event.get_collection(f"{y}_data").find_one({"event_id": id})
            res.pop('_id')

            return {
                "status": True,
                "data": res,
            }

        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return {
                "status": False,
                "message": f"An unexpected error occurred: {e}"
            }


    def get_event_on_month(self, date):
        y, m = date.split("-")
        try:
            # result = eval(f'self.db._{y}.find_one({{"date": f"{m}-{d}"}})')
            s = f'{m}'
            result = self.event.get_collection(y).find({"date": {"$regex": s}})

            result = [res for res in result]
            for res in result:
                res.pop('_id')

            return {
                "status": True,
                "data": result,
            }

        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            return {
                "status": False,
                "message": f"An unexpected error occurred: {e}"
            }


    def add_event(self, data):
        y, m, d = data.date.split('-')
        new = False
        
        try:
            res = self.event.get_collection(y).find_one({'date': f"{m}-{d}"})
            try:
                event = res['event_id']
            except:
                new = True
                res = {
                    'date': f"{m}-{d}",
                    'event_id': []
                }
                event = res['event_id']
            
            new_event = ''.join([y, m, d, str(len(event))])
            event.extend([new_event])

            def object_to_dict(obj):
                if hasattr(obj, '__dict__'):
                    return {key: object_to_dict(value) for key, value in obj.__dict__.items()}
                elif isinstance(obj, list):
                    return [object_to_dict(item) for item in obj]
                else:
                    return obj
            
            data = object_to_dict(data)
            data.update({
                'event_id': new_event
            })

            if new:
                self.event.get_collection(y).insert_one(res)
            else:
                self.event.get_collection(y).update_one({'date': f"{m}-{d}"}, {"$set": res})

            self.event.get_collection(f'{y}_data').insert_one(data)
                
            return True

        except Exception as e:
            print(e)
            return False
        

    def delete_event(self, data):
        y, m, d = data['date'].split('-')
        try:
            self.event.get_collection(y).delete_one({
                'date': f"{m}-{d}",
                'event_id': data['event_id']
            })
            self.event.get_collection(f'{y}_data').delete_one({
                'date': f"{y}-{m}-{d}",
                'event_id': data['event_id']
            })
            return True
        
        except Exception as e:
            return False


    def update_event(self, data):
        y, m, d = data.data.date.split('-')
        try:
            def object_to_dict(obj):
                if hasattr(obj, '__dict__'):
                    return {key: object_to_dict(value) for key, value in obj.__dict__.items()}
                elif isinstance(obj, list):
                    return [object_to_dict(item) for item in obj]
                else:
                    return obj
                
            res = object_to_dict(data.data)
            res.update({'event_id': data.event_id})
            self.event.get_collection(f"{y}_data").update_one({'event_id': data.event_id}, {"$set": res})
            return True
        
        except Exception as e:
            print(e)
            return False
