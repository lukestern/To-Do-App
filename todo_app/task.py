class Task(object):
    def __init__(self, task):
        self.id = task['_id']
        self.title = task['title']
        self.status = task['status']
        self.created = task['created']
        self.last_updated = task['updated']