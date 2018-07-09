import discord
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import getenv

client = discord.Client()

@client.event
async def on_message(message):
    if message.author != client.user:
        await client.send_message(message.channel, message.content)

client.run(getenv('DISCORD_TOKEN'))
