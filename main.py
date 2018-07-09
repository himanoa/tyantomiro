import discord
from dotenv import load_dotenv, find_dotenv
from os import getenv
from re import sub

load_dotenv(find_dotenv())

client = discord.Client()


@client.event
async def on_message(message):
    if [user for user in message.mentions if user == client.user]:
        removed_mention_content = (sub(r'<.+>\s', '', message.content))
        if removed_mention_content.startswith('joinvc'):
            if message.author.voice_channel is None:
                await client.send_message(message.channel, '先にVCに入ってくれ')
            vc = client.get_channel(message.author.voice_channel.id)
            await client.join_voice_channel(vc)


client.run(getenv('DISCORD_TOKEN'))
