from flask import Flask, render_template, url_for, redirect
from flask.globals import request
from todo_app.data.session_items import get_item, get_items, add_item, save_item, remove_item
from todo_app.trello import Trello
from todo_app.views import ViewModel


def create_app():
    app = Flask(__name__)
    trello = Trello()

    @app.route('/')
    def index():
        tasks = get_items(trello)
        task_view_model = ViewModel(tasks)
        return render_template('index.html', view_model = task_view_model)

    @app.route('/add_new', methods=['POST'])    
    def add_new():
        new_task_title = request.form.get('new_task')
        add_item(trello, new_task_title)
        return redirect(url_for('index'))

    @app.route('/finish/<id>')
    def finish_task(id):
        task = get_item(trello, id)
        task.status = 'Complete'
        save_item(trello, task)
        return redirect(url_for('index'))

    @app.route('/start/<id>')
    def start_task(id):
        task = get_item(trello, id)
        task.status = 'In Progress'
        save_item(task)
        return redirect(url_for('index'))

    @app.route('/stop/<id>')
    def stop_task(id):
        task = get_item(trello, id)
        task.status = 'Not Started'
        save_item(task)
        return redirect(url_for('index'))

    @app.route('/delete/<id>')
    def delete_task(id):
        task = get_item(trello, id)
        remove_item(task)
        return redirect(url_for('index'))
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
