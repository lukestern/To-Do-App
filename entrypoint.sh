#!/bin/bash
poetry run gunicorn -b 0.0.0.0:5000 'todo_app.app:create_app()'