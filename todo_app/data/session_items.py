from flask.helpers import stream_with_context
from pymongo.results import UpdateResult
from todo_app.mongo_service import MongoService
from todo_app.task import Task


def get_tasks(mongo_service: MongoService):
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
   
    return mongo_service.get_all_cards()

def get_task(mongo_service: MongoService, id: int) -> Task:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_tasks(mongo_service)

    return next((item for item in items if item.id == id), None)

def add_task(mongo_service: MongoService, title) -> UpdateResult:
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    return mongo_service.create_task(title)

def move_task(mongo_service: MongoService, task: Task, new_state: str):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    match new_state:
        case 'Not Started':
            return mongo_service.move_task_to_not_started(task.id)
        case 'In Progress':
            return mongo_service.move_task_to_in_progress(task.id)
        case 'Complete':
            return mongo_service.move_task_to_complete(task.id)


def remove_task(mongo_service: MongoService, task: Task) -> UpdateResult:
    """
    Removes an existing item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        item: The item to remove.
    """
    return mongo_service.move_task_to_deleted(Task.id)
