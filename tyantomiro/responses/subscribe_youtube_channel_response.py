from .base_response import BaseResponse
from tyantomiro.youtube_api import get_channel, ChannelNotFoundError


async def subscribe_channel(firebase, youtube_key, channel_id, server_id):
    await get_channel(channel_id, youtube_key)
    path = 'youtube_channel/{}'.format(channel_id)
    await firebase.patch(
        path=path,
        value={
            "subscribed_servers": {
                server_id: True
            }
        }
    )


class SubscribeYoutubeChannelResponse(BaseResponse):

    def __init__(self, firebase, youtube_key):
        self.firebase = firebase
        self.youtube_key = youtube_key

    async def execute(self, matched, client, message):
        if message.server is None:
            await client.send_message(
                message.channel,
                '''
                To run this command you need to run it on the published server.
                '''
            )
        if not matched[1]:
            await client.send_message(
                message.channel,
                'Youtube channel Id を指定してください'
            )
        else:
            try:
                await subscribe_channel(
                    self.firebase,
                    self.youtube_key,
                    matched[1],
                    message.server.id
                )
                await client.send_message(
                    message.channel,
                    '{} の購読が開始されました.'.format(matched[1])
                )
            except ChannelNotFoundError:
                await client.send_message(
                    message.channel,
                    '{}はyoutubeのチャンネルIDではありません'.format(matched[1])
                )

    def help(self, client):
        return f"""
**@{client.user} subscribe [channel_id]**

channel_idで指定したチャンネルを購読開始します。
購読開始したチャンネルは以後通知チャンネルに、
生放送が行なわれている場合は通知されます
    """
