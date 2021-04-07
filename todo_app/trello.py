from werkzeug.exceptions import HTTPException
from types import MethodDescriptorType
from dotenv import load_dotenv
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
        url = f"boards/{self.board}/lists"
        result = self.make_api_call_and_check_response(url)
        if result:
            lists = {}
            for lis in result:
                lists[lis['name']] = lis['id']
            return lists

    def get_cards_from_a_list(self, list_id):
        '''
        Returns list of card dictionaries.
        '''
        url = f"lists/{list_id}/cards"
        result = self.make_api_call_and_check_response(url)
        cards = []
        for res in result:
            cards.append(dict((k, res[k]) for k in ('id', 'name', 'idList') if k in res))
        return cards

    def get_all_cards(self):
        cards_in_lists = [self.get_cards_from_a_list(self.list_ids[key]) for key in self.list_ids]
        card_list = list(itertools.chain.from_iterable(cards_in_lists))
        tasks = [Task(card, self.list_ids) for card in card_list]
        return tasks

    def move_card_to_list(self, card_id, card_status):
        data = dict(idList = self.list_ids[card_status])
        url = f"cards/{card_id}"
        return self.make_api_call_and_check_response(url, method='put', data=data)

    def create_new_card(self, name):
        data = dict(idList = self.list_ids['Not Started'], name = name)
        url = f"cards"
        return self.make_api_call_and_check_response(url, method='post', data=data)

    def delete_card(self, card_id):
        url = f"cards/{card_id}"
        return self.make_api_call_and_check_response(url, method='delete')


class Task:
    def __init__(self, trello_card_dict, list_ids):
        self.id = trello_card_dict['id']
        self.title = trello_card_dict['name']
        self.idList = trello_card_dict['idList']
        self.status = self.get_status_from_list_id(list_ids)

    def get_status_from_list_id(self, list_ids):
        for key, value in list_ids.items():
            if self.idList == value:
                return key
