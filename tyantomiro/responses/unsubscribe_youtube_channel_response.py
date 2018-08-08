from .base_response import BaseResponse
from tyantomiro.youtube_api import get_channel, ChannelNotFoundError


delete_endpoint = '''\
youtube_channels/{channel_id}/subscribed_servers/{server_id}\
'''


async def unsubscribe_channel(firebase, youtube_key, channel_id, server_id):
    await get_channel(channel_id, youtube_key)
    path = delete_endpoint.format(
        channel_id=channel_id,
        server_id=server_id
    )
    print(path)
    await firebase.delete(
        path=path
    )


class UnsubscribeYoutubeChannelResponse(BaseResponse):

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
                await unsubscribe_channel(
                    self.firebase,
                    self.youtube_key,
                    matched[1],
                    message.server.id
                )
                await client.send_message(
                    message.channel,
                    '{} の購読を終了しました.'.format(matched[1])
                )
            except ChannelNotFoundError:
                await client.send_message(
                    message.channel,
                    '{}はyoutubeのチャンネルIDではありません'.format(matched[1])
                )

    def help(self, client):
        return f"""
**@{client.user} unsubscribe [channel_id]**

channel_idで指定したチャンネルを購読を終了します。
    """
