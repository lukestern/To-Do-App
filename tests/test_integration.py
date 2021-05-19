from tests.data import get_trello_responses, list_ids_trello_response
from dotenv import find_dotenv, load_dotenv
from todo_app import app
import requests
import pytest


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

class MockResponse(object):
    def __init__(self):
        self.status_code = 200
        self.url = 'http://trello-test.com'
        self.ok = True

class MockCardResponse(MockResponse):
    def __init__(self):
        super().__init__()

    def json(self):
        return get_trello_responses(1)

class MockListResponse(MockResponse):
    def __init__(self):
        super().__init__()

    def json(self):
        return list_ids_trello_response


@pytest.fixture
def mock_request(monkeypatch):

    def mock_response(*args, **kwargs):
        if  "boards/fake_id/lists" in args[1]:
            return MockListResponse()
        if  "cards" in args[1]:
            return MockCardResponse()
            
    monkeypatch.setattr(requests, 'request', mock_response)


def test_index_page(mock_request, client):
    response = client.get('/')

    assert 'Not Started' in response.data.decode()
    assert 'In Progress' in response.data.decode()
    assert 'Complete' in response.data.decode()
    assert 'Test-0' in response.data.decode()
    assert 'Test-1' in response.data.decode()
    assert 'Test-2' in response.data.decode()
