FROM python:3.9.4-slim-buster as base

WORKDIR /app
EXPOSE 5000
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false


FROM base as production
RUN poetry install --no-dev --no-root
COPY . /app/
ENTRYPOINT poetry run gunicorn -b 0.0.0.0:5000 'todo_app.app:create_app()'


FROM base as development
RUN poetry install
COPY . /app/
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000
