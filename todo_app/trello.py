from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
from datetime import datetime
import requests
import itertools
import os 


class Trello:
    def __init__(self):
        load_dotenv()
        self.key = os.environ.get('TRELLO_KEY')
        self.token = os.environ.get('TRELLO_TOKEN')
        self.url = 'https://api.trello.com/1/'
        self.board = os.environ.get('TRELLO_BOARD_ID')
        self.list_ids = self.get_card_list_ids()

    def make_api_call_and_check_response(self, path, method='get', data=None):
        complete_url = f"{self.url}" + path + f"?key={self.key}&token={self.token}"
        resp = requests.request(method, complete_url, data=data)
        if resp.ok:
            return resp.json()
        else:
            raise HTTPException(f'API call to Trello failed. Error code {resp.status_code}')

    def get_card_list_ids(self):
        '''
        Returns a dictionary where keys are the list names and the values are list ids.
        '''
        path = f"boards/{self.board}/lists"
        result = self.make_api_call_and_check_response(path)
        if result:
            lists = {}
            for lis in result:
                lists[lis['name']] = lis['id']
            return lists

    def get_cards_from_a_list(self, list_id):
        '''
        Returns list of card dictionaries.
        '''
        path = f"lists/{list_id}/cards"
        result = self.make_api_call_and_check_response(path)
        cards = []
        for res in result:
            cards.append(dict((k, res[k]) for k in ('id', 'name', 'idList', 'dateLastActivity') if k in res))
        return cards

    def get_all_cards(self):
        cards_in_lists = [self.get_cards_from_a_list(self.list_ids[key]) for key in self.list_ids]
        card_list = list(itertools.chain.from_iterable(cards_in_lists))
        tasks = [Task(card, self.list_ids) for card in card_list]
        return tasks

    def move_card_to_list(self, card_id, card_status):
        data = dict(idList = self.list_ids[card_status])
        path = f"cards/{card_id}"
        return self.make_api_call_and_check_response(path, method='put', data=data)

    def create_new_card(self, name):
        data = dict(idList = self.list_ids['Not Started'], name = name)
        path = f"cards"
        return self.make_api_call_and_check_response(path, method='post', data=data)

    def delete_card(self, card_id):
        path = f"cards/{card_id}"
        return self.make_api_call_and_check_response(path, method='delete')

    def create_board_with_lists(self, name):
        board = self.create_board(name)
        names = ['Not Started', 'In Progress', 'Complete']
        for name in names:
            self.create_list(board['id'], name)

        return board

    def create_board(self, name):
        data = dict(name = name)
        path = f"boards"
        return self.make_api_call_and_check_response(path, method='post', data=data)

    def delete_board(self, board_id):
        path = f"boards/{board_id}"
        return self.make_api_call_and_check_response(path, method='delete')

    def create_list(self, board_id, name):
        data = dict(name = name)
        path = f"boards/{board_id}/lists"
        return self.make_api_call_and_check_response(path, method='post', data=data)


class Task:
    def __init__(self, trello_card_dict, list_ids):
        self.id = trello_card_dict['id']
        self.title = trello_card_dict['name']
        self.idList = trello_card_dict['idList']
        self.last_active = datetime.strptime(trello_card_dict['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.status = self.get_status_from_list_id(list_ids)

    def get_status_from_list_id(self, list_ids):
        for key, value in list_ids.items():
            if self.idList == value:
                return key
