import discord
import aiofirebase
from os import getenv

from tyantomiro.matcher import create_matcher
from tyantomiro.responses.pong_response import PongResponse
from tyantomiro.responses.help_response import HelpResponse
from tyantomiro.responses.change_notify_channel_response import (
    ChangeNotifyChannelResponse
)
from tyantomiro.tasks import (create_clean_read_notification,
                              create_fetch_youtube_api)

firebase = aiofirebase.FirebaseHTTP("https://{}.firebaseio.com/"
                                    .format(getenv('FIREBASE_ID')))

responses = [
    {"pattern": r'^ping', "response": PongResponse()},
    {"pattern": r'^set_notify',
     "response": ChangeNotifyChannelResponse(firebase)}
]
responses.append({"pattern": r'^help', "response": HelpResponse(responses)})


read_notifaction = []
client = discord.Client()
subscribed_channel_ids = getenv("SUBSCRIBED_CHANNNEL_IDS").split(',')
notify_channel_id = getenv("NOTIFY_CHANNEL_ID")


matcher = create_matcher(responses)


client.loop.create_task(
    create_clean_read_notification(client,
                                   read_notifaction)())
client.loop.create_task(
    create_fetch_youtube_api(client,
                             subscribed_channel_ids,
                             discord.Object(id=notify_channel_id),
                             getenv('YOUTUBE_TOKEN'),
                             read_notifaction)()
)


@client.event
async def on_server_join(server):
    print('server joined')
    print(type(server))
    params = {
        'subscribed_channel': [],
        'notify_channel_id': '',
    }
    await firebase.put(
        path="server/{}".format(server.id),
        value=params
    )


@client.event
async def on_message(message):
    print(message.server.id)
    await matcher(message, client)

client.run(getenv('DISCORD_TOKEN'))
