from requests import get
from dotenv import load_dotenv, find_dotenv
from os import getenv
from pprint import pprint

load_dotenv(find_dotenv())

api_url = 'https://www.googleapis.com/youtube/v3/search'


def build_params(channel_id, key=getenv('YOUTUBE_TOKEN')):
    return {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'eventType': 'live',
        'key': key
    }


lives = (get(api_url, params=build_params('UCdn5BQ06XqgXoAxIhbqw5Rg')).json()
         .get('items'))

pprint(lives)
