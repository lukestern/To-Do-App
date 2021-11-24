from typing import List
from todo_app.task import Task
from bson.objectid import ObjectId
from datetime import datetime

# Functions to generate test task objects.
def get_complete_test_tasks(n: int) -> List[Task]:
    return get_test_tasks(n, 'Complete')

def get_test_tasks(n: int, status: str) -> List[Task]:
    # Produces 2n tasks. Half completed today, half completed on previous date.
    complete_card_dicts = []
    for i in range(1, 2*(n+1)):
        if i in range(1, n+1):
            complete_card_dicts.append(
                {
                    '_id': ObjectId(str(i) + '0' * (24 - len(str(i)))),
                    'title': f'Test-{i}', 
                    'status': status, 
                    'updated': previous_date,
                    'created': creation_date
                }
            )
        elif i in range(n, 2*(n+2)):
            complete_card_dicts.append(
                {
                    '_id': ObjectId(str(i) + '0' * (24 - len(str(i)))),
                    'title': f'Test-{i}', 
                    'status': status, 
                    'updated': today,
                    'created': creation_date
                }
            )
    return get_test_task_objects(complete_card_dicts)

def get_test_task_objects(task_dicts: dict) -> List[Task]:
    # Takes list of mongo response dictionaries and returns list of Task Objects.
    tasks = []
    for task_dict in task_dicts:
        tasks.append(Task(task_dict))
    return tasks


def get_mongo_responses(m: int) -> List[dict]:
    result = create_mongo_responses(0, m, 'a')
    result += create_mongo_responses(m, 2*m, 'b')
    result += create_mongo_responses(2*m, 3*m, 'c')
    return result


def create_mongo_responses(n: int, m: int, status: str) -> List[dict]:
    responses = []
    for i in range(n, m):
        responses.append({
            '_id': ObjectId(str(i) + '0' * (24 - len(str(i)))),
            "title": f'Test-{i}',
            "status": status,
            "created": today,
            "updated": today,
        })
    return responses

#Test data.

creation_date = datetime(2020, 4, 7, 12, 45, 00)
previous_date = datetime(2021, 4, 7, 11, 55, 29)
today = datetime.today()

sample_data = [
    {
        '_id': ObjectId('1' + '0' * 23), 
        'title': 'Test-1', 
        'status': 'Not Started', 
        'created': creation_date, 
        'updated': previous_date
    },
    {
        '_id': ObjectId('2' + '0' * 23), 
        'title': 'Test-2', 
        'status': 'In Progress', 
        'created': creation_date, 
        'updated': previous_date
    },
    {
        '_id': ObjectId('3' + '0' * 23), 
        'title': 'Test-3', 
        'status': 'Complete', 
        'created': creation_date, 
        'updated': previous_date
    }
]






