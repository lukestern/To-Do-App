from todo_app.views import ViewModel
from tests.data import previous_date, todays_date, today, trello_card_dicts, get_complete_test_tasks, get_test_task_objects

def test_return_all_cards():
    tasks = get_test_task_objects(trello_card_dicts)

    result = ViewModel(tasks).tasks

    assert result == tasks


def test_return_all_cards_returns_none():
    tasks = []

    result = ViewModel(tasks).tasks

    assert result == []

def test_return_not_started_tasks():
    tasks = get_test_task_objects(trello_card_dicts)

    result = ViewModel(tasks).not_started_tasks

    for task in result:
        assert task.status == 'Not Started'


def test_return_no_not_started_tasks():
    tasks = []

    result = ViewModel(tasks).not_started_tasks

    assert result == []


def test_return_in_progress_tasks():
    tasks = get_test_task_objects(trello_card_dicts)

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
    tasks = get_test_task_objects(trello_card_dicts)

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