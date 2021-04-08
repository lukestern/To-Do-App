def get_items(trello):
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
   
    return trello.get_all_cards()

def get_item(trello, id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items(trello)

    return next((item for item in items if item.id == id), None)

def add_item(trello, title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    trello.create_new_card(title)

    return title

def save_item(trello, item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    trello.move_card_to_list(item.id, item.status)
    return item

def remove_item(trello, item):
    """
    Removes an existing item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        item: The item to remove.
    """
    trello.delete_card(item.id)

    return item
