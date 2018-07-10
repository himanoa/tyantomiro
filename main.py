import discord
import asyncio
from dotenv import load_dotenv, find_dotenv
from os import getenv
from re import sub
from requests import get


load_dotenv(find_dotenv())

api_url = 'https://www.googleapis.com/youtube/v3/search'

read_notifaction = []

with open('./list', 'r') as file:
    channel_ids = file.read().split('\n')[0:-1]
    print(file.read().split('\n'))

    client = discord.Client()

    def build_params(channel_id, key=getenv('YOUTUBE_TOKEN')):
        return {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'eventType': 'live',
            'key': key
        }

    def play_sound():
        sound_file = './vtuber_notification.wav'

        if client.voice_clients:
            (list(client.voice_clients)[0]
             .create_ffmpeg_player(sound_file).start())

    async def fetch_youtube_api():
        channel_url = "https://www.youtube.com/channel/{}/live"
        await client.wait_until_ready()
        notify_channel = discord.Object(id=getenv('CHANNEL_ID'))
        interval_minutes = 60 * 5  # 5分おきに
        print(channel_ids)
        while not client.is_closed:
            for channel_id in channel_ids:
                if channel_id in read_notifaction:
                    continue
                items = (get(api_url, build_params(channel_id))
                         .json().get('items'))
                if items:
                    play_sound()
                    await client.send_message(notify_channel,
                                              channel_url.format(channel_id))
                    read_notifaction.append(channel_id)
            await asyncio.sleep(interval_minutes)

    @client.event
    async def on_message(message):
        if [user for user in message.mentions if user == client.user]:
            removed_mention_content = (sub(r'<.+>\s', '', message.content))
            if removed_mention_content.startswith('joinvc'):
                print(client.voice_clients)
                if message.author.voice_channel is None:
                    await client.send_message(message.channel,
                                              '先にVCに入ってくれ')
                vc = client.get_channel(message.author.voice_channel.id)
                await client.join_voice_channel(vc)

    client.loop.create_task((fetch_youtube_api()))
    client.run(getenv('DISCORD_TOKEN'))
