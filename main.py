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
        if message.author != client.user:
            await client.send_message(message.channel, removed_mention_content)

client.run(getenv('DISCORD_TOKEN'))
