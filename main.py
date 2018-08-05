import discord
from dotenv import load_dotenv, find_dotenv
from os import getenv

from tyantomiro.matcher import create_matcher
from tyantomiro.responses.pong_response import PongResponse

responses = [
    {"pattern": r'^ping', "response": PongResponse()}
]

matcher = create_matcher(responses)
load_dotenv(find_dotenv())


read_notifaction = []

client = discord.Client()


@client.event
async def on_message(message):
    await matcher(message, client)


client.run(getenv('DISCORD_TOKEN'))
