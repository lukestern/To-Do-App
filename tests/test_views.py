from todo_app.trello import Task
from todo_app.views import ViewModel
from datetime import datetime


# Test data.
list_ids = {'Not Started': 'a', 'In Progress': 'b', 'Complete': 'c'}

previous_date = '2021-04-07T11:55:29.179000Z'
today = datetime.today()
todays_date = today.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

trello_card_dicts = [
    {'id': '1', 'name': 'Test-1', 'idList': 'a', 'status': 'Not Started', 'dateLastActivity': previous_date},
    {'id': '2', 'name': 'Test-2', 'idList': 'b', 'status': 'In Progress', 'dateLastActivity': previous_date},
    {'id': '3', 'name': 'Test-3', 'idList': 'c', 'status': 'Complete', 'dateLastActivity': previous_date}
]


# Functions to generate test task objects.
def get_complete_test_tasks(n):
    # Produces 2n tasks. Half completed today, half completed on previous date.
    complete_card_dicts = []
    for i in range(0, 2*n):
        if i in range(0, n):
            complete_card_dicts.append(
                {'id': str(i), 'name': f'Test-{i}', 'idList': 'c', 'status': 'Complete', 'dateLastActivity': previous_date}
            )
        elif i in range(n, 2*n+1):
            complete_card_dicts.append(
                {'id': str(i), 'name': f'Test-{i}', 'idList': 'c', 'status': 'Complete', 'dateLastActivity': todays_date}
            )
    return get_test_tasks(complete_card_dicts)

def get_test_tasks(task_dicts):
    # Takes list of Trello dictionaries and returns list of Task Objects.
    tasks = []
    for card_dict in task_dicts:
        tasks.append(Task(card_dict, list_ids))
    return tasks


def test_return_all_cards():
    tasks = get_test_tasks(trello_card_dicts)

    result = ViewModel(tasks).tasks

    assert result == tasks


def test_return_all_cards_returns_none():
    tasks = []

    result = ViewModel(tasks).tasks

    assert result == []

def test_return_not_started_tasks():
    tasks = get_test_tasks(trello_card_dicts)

    result = ViewModel(tasks).not_started_tasks

    for task in result:
        assert task.status == 'Not Started'


def test_return_no_not_started_tasks():
    tasks = []

    result = ViewModel(tasks).not_started_tasks

    assert result == []


def test_return_in_progress_tasks():
    tasks = get_test_tasks(trello_card_dicts)

    result = ViewModel(tasks).in_progress_tasks

    for task in result:
        assert task.status == 'In Progress'


def test_return_no_in_progress_tasks():
    tasks = []

    result = ViewModel(tasks).in_progress_tasks

    assert result == []


def test_more_than_5_complete_tasks():
    tasks = get_complete_test_tasks(5)

    assert ViewModel(tasks).more_than_5_complete_tasks

def test_less_than_5_complete_tasks():
    tasks = get_complete_test_tasks(2)

    assert not ViewModel(tasks).more_than_5_complete_tasks

def test_return_complete_tasks():
    tasks = get_test_tasks(trello_card_dicts)

    result = ViewModel(tasks).complete_tasks

    for task in result:
        assert task.status == 'Complete'


def test_return_no_complete_tasks():
    tasks = []

    result = ViewModel(tasks).complete_tasks

    assert result == []


def test_complete_tasks_returns_tasks_completed_today():
    tasks = get_complete_test_tasks(6)

    result = ViewModel(tasks).complete_tasks

    for task in result:
        assert task.last_active.strftime('%Y-%m-%dT%H:%M:%S.%fZ') == todays_date


def test_complete_tasks_returns_all_tasks():
    tasks = get_complete_test_tasks(2)

    result = ViewModel(tasks).complete_tasks

    assert len(result) == 4


def test_return_older_tasks():
    tasks = get_complete_test_tasks(5)

    result = ViewModel(tasks).older_tasks

    for task in result:
        assert task.last_active.strftime('%Y-%m-%dT%H:%M:%S.%fZ') == previous_date


def test_return_tasks_completed_today():
    tasks = get_complete_test_tasks(5)

    result = ViewModel(tasks).tasks_completed_today()

    for task in result:
        assert task.last_active.date() == today.date()