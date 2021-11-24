import os
from flask import Flask, render_template, url_for, redirect
from flask.globals import request
from todo_app.data.session_items import get_task, get_tasks, add_task, update_task_status
from todo_app.mongo_service import MongoService
from todo_app.views import ViewModel


def create_app(db_name = os.environ.get("DB_NAME")):
    app = Flask(__name__)
    mongo = MongoService(db_name)

    @app.route('/')
    def index():
        tasks = get_tasks(mongo)
        task_view_model = ViewModel(tasks)
        return render_template('index.html', view_model = task_view_model)

    @app.route('/add_new', methods=['POST'])    
    def add_new():
        new_task_title = request.form.get('new_task')
        add_task(mongo, new_task_title)
        return redirect(url_for('index'))

    @app.route('/finish/<id>')
    def finish_task(id):
        task = get_task(mongo, id)
        task.status = 'Complete'
        update_task_status(mongo, task)
        return redirect(url_for('index'))

    @app.route('/start/<id>')
    def start_task(id):
        task = get_task(mongo, id)
        task.status = 'In Progress'
        update_task_status(mongo, task)
        return redirect(url_for('index'))

    @app.route('/stop/<id>')
    def stop_task(id):
        task = get_task(mongo, id)
        task.status = 'Not Started'
        update_task_status(mongo, task)
        return redirect(url_for('index'))

    @app.route('/delete/<id>')
    def delete_task(id):
        task = get_task(mongo, id)
        task.status = 'Deleted'
        update_task_status(mongo, task)
        return redirect(url_for('index'))
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
