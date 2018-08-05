import discord
from os import getenv

from tyantomiro.matcher import create_matcher
from tyantomiro.responses.pong_response import PongResponse
from tyantomiro.tasks import (create_clean_read_notification,
                              create_fetch_youtube_api)

responses = [
    {"pattern": r'^ping', "response": PongResponse()}
]

matcher = create_matcher(responses)

read_notifaction = []

client = discord.Client()


@client.event
async def on_message(message):
    await matcher(message, client)


client.loop.create_task(
    create_clean_read_notification(client,
                                   read_notifaction)())
client.loop.create_task(
    create_fetch_youtube_api(client,
                             [],
                             discord.Object(id="asadsad"),
                             getenv('YOUTUBE_KEY'),
                             read_notifaction)()
)
client.run(getenv('DISCORD_TOKEN'))
