import asyncio
from discord import Object
from tyantomiro.youtube_api import search_living_channel, build_params


channel_url = "https://www.youtube.com/channel/{}/live"

def create_discord_task(client, task_function):
    async def _task(*args):
        await client.wait_until_ready()
        while not client.is_closed:
            await task_function(*args)
    return _task


async def notify_task(client, firebase, server_id, channel_id):
    server = await firebase.get(path='server/{}'.format(server_id))
    if server:
        if server.get('send_notifications', {}).get(channel_id):
            return
        await client.send_message(
            Object(id=server.get('notify_channel_id')),
            channel_url.format(channel_id)
        )
        await firebase.patch(
            path='server/{}/send_notifications',
            value={
                channel_id: True
            }
        )

async def fetch_task(
    client,
    channel_id,
    subscribed_servers,
    youtube_key,
    firebase
):
    items = await search_living_channel(channel_id, youtube_key)
    if items:
        for server_id in subscribed_servers:
            client.loop.create_task(
                notify_task(client, firebase, server_id, channel_id)
            )


async def fork_fetch_task(client, firebase, youtube_key):
    channels = await firebase.get(
        path='youtube_channels'
    )
    for channel_id in channels.keys():
        subscribed_servers = channels.get(channel_id).get('subscribed_servers')
        client.loop.create_task(
            fetch_task(
                client,
                channel_id,
                subscribed_servers,
                youtube_key,
                firebase
            )
        )

def create_notify_channel_task(client, firebase, youtube_key):
    interval_minutes = 60 * 5  # 5分おきに
    async def _task():
        await fork_fetch_task(client, firebase, youtube_key)
        await asyncio.sleep(interval_minutes)
    return create_discord_task(client, _task)


def create_clean_send_notifycation(client, firebase):

    async def clean_send_notification():
        await client.wait_until_ready()
        while not client.is_closed:
            await asyncio.sleep(60 * 60)
            servers = await firebase.get(path='servers')
            for server_id in servers.keys():
                await firebase.put(
                    path='servers/{}/send_notifications',
                    value={}
                )

    return clean_send_notification
