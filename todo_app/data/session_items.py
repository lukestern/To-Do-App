from todo_app.trello import Trello

global t
t = Trello()


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
   
    return t.get_all_cards()

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()

    return next((item for item in items if item.id == id), None)

def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    t.create_new_card(title)

    return title

def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    t.move_card_to_list(item.id, item.status)
    return item

def remove_item(item):
    """
    Removes an existing item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        item: The item to remove.
    """
    t.delete_card(item.id)

    return item
