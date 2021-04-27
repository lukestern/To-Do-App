# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

### Trello Setup 

Trello is used to store the tasks displayed in the app. 
- Set up an account on Trello. https://trello.com/signup
- Add your API key to .env. https://trello.com/app-key
- Add your token to .env. https://trello.com/1/token/approve
- Create a Trello board. https://trello.com/en-GB/guide/create-a-board
- Add your board ID to .env. This can be found in the URL of your board. (https://trello.com/b/<board_id>/to-do-app)

### VirtualBox

- Install VirtualBox. https://www.virtualbox.org/

### Vagrant

- Install Vagrant. https://www.vagrantup.com/downloads

### Docker 

- Install Docker. https://docs.docker.com/get-docker/


## Running the App (Production)

### Option 1 - Docker
```bash
docker compose up --build
```

### Option 2 - Vagrant
```bash
$ vagrant up
```


## Running the App (Development)
Once the all dependencies have been installed, start the Flask app in development mode.

### Option 1 - Docker
```bash
docker compose -f .\docker-compose-dev.yml up --build
```

### Option 2 - Poetry
```bash
poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running Tests

### Option 1 - Poetry
```bash
# Unit and Integration tests
poetry run pytest .\tests\
# End to end tests
poetry run pytest .\tests_end_to_end\
```

### Option 2 - Docker
```bash
# Unit, integration and end to end tests
docker compose -f .\docker-compose-test.yml up --build
```