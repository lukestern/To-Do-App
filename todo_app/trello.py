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

    def get_and_check_response(self, url, method='get', body=None):
        complete_url = f"{self.url}" + url + f"?key={self.key}&token={self.token}"
        resp = eval("requests." + method.lower() + "('" + complete_url + "')")
        if resp.status_code == 200:
            # return json.dumps(resp.json(), indent=4)
            return resp.json()

    def get_card_list_ids(self):
        url = f"boards/{self.board}/lists"
        result = self.get_and_check_response(url)
        if result:
            lists = {}
            for lis in result:
                lists[lis['name']] = lis['id']
            return  lists

    def get_cards_from_a_list(self, list_id):
        url = f"lists/{list_id}/cards"
        return self.get_and_check_response(url)

    def get_all_cards(self):
        list_ids = self.get_card_list_ids()
        cards_in_lists = [self.get_cards_from_a_list(list_ids[key]) for key in list_ids]
        return list(itertools.chain.from_iterable(cards_in_lists))

    def update_card(self, card_id, update_dictionary):
        url = f"cards/{card_id}"
        return self.get_and_check_response(url)
