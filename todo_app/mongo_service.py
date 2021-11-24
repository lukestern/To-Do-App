from datetime import datetime
from typing import List
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from todo_app.task import Task
import pymongo
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

class MongoService:
    def __init__(self, db_name: str):
        client = self._connect_to_client(db_name)
        self.task_collection = client[db_name].tasks

    @staticmethod
    def _connect_to_client(db_name: str) -> MongoClient: 
        load_dotenv()
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_USER_PASSWORD")
        cluster_url = os.environ.get("CLUSTER_URL")
        return pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{cluster_url}/{db_name}?ssl=true&retryWrites=true&w=majority")

    def get_tasks(self) -> List[Task]:
        tasks = []
        for task in self.task_collection.find():
            tasks.append(Task(task))
        return tasks

    def create_task(self, title: str) -> InsertOneResult:
        details = {
            'title': title,
            'status': 'Not Started',
            'created': datetime.now(),
            'updated': datetime.now()
        }
        return self.task_collection.insert_one(details)

    def update_task(self, id: int, values_to_update: dict) -> UpdateResult:
        return self.task_collection.update_one({'_id': ObjectId(id)}, values_to_update)
    
    def change_task_status(self, task: Task) -> UpdateResult:
        return self.update_task(task.id, {'$set': {'status': task.status, 'updated': datetime.now()}})

    # Methods for end to end testing
    @staticmethod
    def delete_database(db_name: str):
        MongoService(db_name).task_collection.drop()

