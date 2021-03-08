from types import MethodDescriptorType
from dotenv import load_dotenv
import requests
import itertools
import json
import os 


class Trello:
    def __init__(self):
        load_dotenv()
        self.key = os.environ.get('TRELLO_KEY')
        self.token = os.environ.get('TRELLO_TOKEN')
        self.url = os.environ.get('TRELLO_BASE_URL')
        self.board = os.environ.get('TRELLO_BOARD_ID')
        self.username = os.environ.get('TRELLO_USER')
        self.list_ids = self.get_card_list_ids()

    def make_api_call_and_check_response(self, url, method='get', data=None):
        complete_url = f"{self.url}" + url + f"?key={self.key}&token={self.token}"
        resp = eval("requests." + method.lower() + "('" + complete_url + "', data=" + str(data) + ")")
        if resp.status_code == 200:
            # print(json.dumps(resp.json(), indent=4))
            return resp.json()

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
            return  lists

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
        return self.add_status_to_cards_in_list(card_list)

    def add_status_to_cards_in_list(self, card_list):
        for card in card_list:
            for key, value in self.list_ids.items():
                if card['idList'] == value:
                    card['status'] = key
        return card_list

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
