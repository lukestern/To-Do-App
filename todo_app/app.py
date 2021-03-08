from flask import Flask, render_template, url_for, redirect
from flask.globals import request
from todo_app.data.session_items import get_item, get_items, add_item, save_item, remove_item
from todo_app.flask_config import Config
from flask.json import JSONEncoder
from todo_app.trello import Task


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            task_dict = {
                "id": obj.id,
                "title": obj.title,
                "status": obj.status,
                "idList": obj.idList
            }
            return task_dict
        else:
            JSONEncoder.default(self, obj)

app = Flask(__name__)
app.config.from_object(Config)
app.json_encoder = CustomJSONEncoder

@app.route('/')
def index():
    return render_template('index.html', tasks = get_items())

@app.route('/sortby/<sort>')
def sortby(sort):
    items = get_items()
    if 'done' in sort:
        tasks = sorted(items, key=lambda k: k['status']) 
    elif 'todo' in sort:
        tasks = sorted(items, key=lambda k: k['status'], reverse=True) 
    return render_template('index.html', tasks = tasks, all=True)

@app.route('/view/<type>')
def view_task_type(type):
    items = get_items()
    if 'all' in type:
        return redirect(url_for('index'))
    elif 'complete' in type:
        tasks = [item for item in items if 'Complete' in item['status']]
    elif 'started' in type:
        tasks = [item for item in items if 'In Progress' in item['status']]
    elif 'todo' in type:
        tasks = [item for item in items if 'Not Started' in item['status']]
    return render_template('index.html', tasks = tasks, all = False)

@app.route('/add_new', methods=['POST'])    
def add_new():
    new_task_title = request.form.get('new_task')
    add_item(new_task_title)
    return redirect(url_for('index'))

@app.route('/finish/<id>')
def finish_task(id):
    task = get_item(id)
    task['status'] = 'Complete'
    save_item(task)
    return redirect(url_for('index'))

@app.route('/start/<id>')
def start_task(id):
    task = get_item(id)
    task['status'] = 'In Progress'
    save_item(task)
    return redirect(url_for('index'))

@app.route('/stop/<id>')
def stop_task(id):
    task = get_item(id)
    task['status'] = 'Not Started'
    save_item(task)
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_task(id):
    task = get_item(id)
    remove_item(task)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
