import pymongo
from pymongo.mongo_client import MongoClient
from tests.data import sample_data
from dotenv import find_dotenv, load_dotenv
from todo_app import app
import pytest
import mongomock
from todo_app.mongo_service import MongoService
from todo_app.task import Task


@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    monkeypatch.setattr(pymongo, 'MongoClient', mongomock.MongoClient)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

@pytest.fixture
def mock_request(monkeypatch):
    def mock_tasks(*args, **kwargs):
        return [Task(task) for task in sample_data]
            
    monkeypatch.setattr(MongoService, 'get_tasks', mock_tasks)


def test_index_page(mock_request, client):
    response = client.get('/')

    assert 'Not Started' in response.data.decode()
    assert 'In Progress' in response.data.decode()
    assert 'Complete' in response.data.decode()
    assert 'Test-1' in response.data.decode()
    assert 'Test-2' in response.data.decode()
    assert 'Test-3' in response.data.decode()
