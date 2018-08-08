import asyncio
from tyantomiro.youtube_api import search_living_channel

api_url = 'https://www.googleapis.com/youtube/v3/search'


def build_params(channel_id, key):
    return {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'eventType': 'live',
        'key': key
    }


def create_fetch_youtube_api(
    client,
    channel_ids,
    notify_channel_id,
    youtube_key,
    read_notifaction
):

    async def fetch_youtube_api():
        channel_url = "https://www.youtube.com/channel/{}/live"
        await client.wait_until_ready()
        interval_minutes = 60 * 5  # 5分おきに
        while not client.is_closed:
            for channel_id in channel_ids:
                if channel_id in read_notifaction:
                    continue
                if await search_living_channel(channel_id, youtube_key):
                    await client.send_message(
                        notify_channel_id,
                        channel_url.format(
                            channel_id
                        )
                    )
                    read_notifaction.append(channel_id)
            await asyncio.sleep(interval_minutes)
    return fetch_youtube_api


def create_clean_read_notification(client, read_notifaction):

    async def clean_read_notification():
        await client.wait_until_ready()
        while not client.is_closed:
            global read_notifaction
            read_notifaction = []
            await asyncio.sleep(60 * 60)

    return clean_read_notification
