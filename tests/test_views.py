from todo_app.trello import Task
from todo_app.views import ViewModel

list_ids = {'Not Started': 'a', 'In Progress': 'b', 'Complete': 'c'}

trello_card_dicts = [
    {'id': '1', 'name': 'Test-1', 'idList': 'a', 'status': 'Not Started'},
    {'id': '2', 'name': 'Test-2', 'idList': 'b', 'status': 'In Progress'},
    {'id': '3', 'name': 'Test-3', 'idList': 'c', 'status': 'Complete'}
]

def get_test_tasks():
    tasks = []
    for card_dict in trello_card_dicts:
        tasks.append(Task(card_dict, list_ids))
    return tasks


def test_return_all_cards():
    tasks = get_test_tasks()

    result = ViewModel(tasks).tasks

    assert result == tasks


def test_return_all_cards_returns_none():
    tasks = []

    result = ViewModel(tasks).tasks

    assert result == []

def test_return_not_started_tasks():
    tasks = get_test_tasks()

    result = ViewModel(tasks).not_started_tasks

    for task in result:
        assert task.status == 'Not Started'


def test_return_no_not_started_tasks():
    tasks = []

    result = ViewModel(tasks).not_started_tasks

    assert result == []


def test_return_in_progress_tasks():
    tasks = get_test_tasks()

    result = ViewModel(tasks).in_progress_tasks

    for task in result:
        assert task.status == 'In Progress'


def test_return_no_in_progress_tasks():
    tasks = []

    result = ViewModel(tasks).in_progress_tasks

    assert result == []


def test_return_complete_tasks():
    tasks = get_test_tasks()

    result = ViewModel(tasks).complete_tasks

    for task in result:
        assert task.status == 'Complete'

def test_return_no_complete_tasks():
    tasks = []

    result = ViewModel(tasks).complete_tasks

    assert result == []
