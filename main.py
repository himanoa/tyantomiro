import discord
import asyncio
from dotenv import load_dotenv, find_dotenv
from os import getenv
from re import sub
from requests import get
from pprint import pprint


load_dotenv(find_dotenv())

api_url = 'https://www.googleapis.com/youtube/v3/search'

with open('./list', 'r') as file:
    channel_ids = file.read().split('\n')[0:1]

    client = discord.Client()

    def build_params(channel_id, key=getenv('YOUTUBE_TOKEN')):
        return {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'eventType': 'live',
            'key': key
        }

    async def fetch_youtube_api():
        await client.wait_until_ready()
        notify_channel = discord.Object(id=getenv('CHANNEL_ID'))
        interval_minutes = 60 * 5 # 5分おきに
        print(channel_ids)
        while not client.is_closed:
            for channel_id in channel_ids:
                items = get(api_url, build_params(channel_id)).json().get('items')
                pprint(items)
                if items:
                    await client.send_message(notify_channel,
                                              "https://www.youtube.com/channel/{}/live".format(items[0]['snippet']['channelId']))
            await asyncio.sleep(interval_minutes)

    @client.event
    async def on_message(message):
        if [user for user in message.mentions if user == client.user]:
            removed_mention_content = (sub(r'<.+>\s', '', message.content))
            if removed_mention_content.startswith('joinvc'):
                if message.author.voice_channel is None:
                    await client.send_message(message.channel, '先にVCに入ってくれ')
                vc = client.get_channel(message.author.voice_channel.id)
                await client.join_voice_channel(vc)


    client.loop.create_task((fetch_youtube_api()))
    client.run(getenv('DISCORD_TOKEN'))
