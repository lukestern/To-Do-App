from todo_app.trello import Task
from datetime import datetime

# Functions to generate test task objects.
def get_complete_test_tasks(n):
    return get_test_tasks(n, 'c', 'Complete')


def get_test_tasks(n, list_id, status):
    # Produces 2n tasks. Half completed today, half completed on previous date.
    complete_card_dicts = []
    for i in range(0, 2*n):
        if i in range(0, n):
            complete_card_dicts.append(
                {'id': str(i), 'name': f'Test-{i}', 'idList': list_id, 'status': status, 'dateLastActivity': previous_date}
            )
        elif i in range(n, 2*n+1):
            complete_card_dicts.append(
                {'id': str(i), 'name': f'Test-{i}', 'idList': list_id, 'status': status, 'dateLastActivity': todays_date}
            )
    return get_test_task_objects(complete_card_dicts)


def get_test_task_objects(task_dicts):
    # Takes list of Trello dictionaries and returns list of Task Objects.
    tasks = []
    for card_dict in task_dicts:
        tasks.append(Task(card_dict, list_ids))
    return tasks


def get_trello_responses(m):
    result = create_trello_responses(0, m, 'a')
    result += create_trello_responses(m, 2*m, 'b')
    result += create_trello_responses(2*m, 3*m, 'c')
    return result


def create_trello_responses(n, m, list_id):
    responses = []
    for i in range(n, m):
        responses.append({
            "id": str(i),
            "dateLastActivity": todays_date,
            "idBoard": 'fake_id',
            "idList": list_id,
            "name": f'Test-{i}',
            "idMembersVoted": []
        })
    return responses

#Test data.
list_ids = {'Not Started': 'a', 'In Progress': 'b', 'Complete': 'c'}

list_ids_trello_response = [
    {
        "id": "a",
        "name": "Not Started",
        "idBoard": "fake_id"
    },
    {
        "id": "b",
        "name": "In Progress",
        "idBoard": "fake_id"
    },
    {
        "id": "c",
        "name": "Complete",
        "idBoard": "fake_id"
    }
]

previous_date = '2021-04-07T11:55:29.179000Z'
today = datetime.today()
todays_date = today.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

trello_card_dicts = [
    {'id': '1', 'name': 'Test-1', 'idList': 'a', 'status': 'Not Started', 'dateLastActivity': previous_date},
    {'id': '2', 'name': 'Test-2', 'idList': 'b', 'status': 'In Progress', 'dateLastActivity': previous_date},
    {'id': '3', 'name': 'Test-3', 'idList': 'c', 'status': 'Complete', 'dateLastActivity': previous_date}
]






