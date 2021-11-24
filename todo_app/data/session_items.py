from bson.objectid import ObjectId
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
   
    return mongo_service.get_tasks()

def get_task(mongo_service: MongoService, id: int) -> Task:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    tasks = get_tasks(mongo_service)

    return next((task for task in tasks if task.id == ObjectId(id)), None)

def add_task(mongo_service: MongoService, title) -> UpdateResult:
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    return mongo_service.create_task(title)

def update_task_status(mongo_service: MongoService, task: Task) -> UpdateResult:
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    return mongo_service.change_task_status(task)
