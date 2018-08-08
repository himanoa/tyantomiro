import aiohttp

api_url = 'https://www.googleapis.com/youtube/v3/{}'
search_api_url = api_url.format('search')
list_api_url = api_url.format('channels')


class ChannelNotFoundError(Exception):
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def __str__(self):
        return "{} is NotFound".format(self.channel_id)


def build_params(channel_id, key):
    return {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'eventType': 'live',
        'key': key
    }


async def get_channel(channel_id, youtube_key):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            list_api_url,
            params={
                'part': 'id',
                'id': channel_id,
                'key': youtube_key
            }
        ) as r:
            items = (await r.json()).get('items')
            if not items:
                raise ChannelNotFoundError(channel_id)
            return (await r.json()).get('items')


async def search_living_channel(channel_id, youtube_key):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            search_api_url,
            params=build_params(channel_id, youtube_key)
        ) as r:
            return (await r.json()).get('items')
