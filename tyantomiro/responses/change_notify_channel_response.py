from .base_response import BaseResponse


class ChangeNotifyChannelResponse(BaseResponse):

    def __init__(self, firebase):
        self.firebase = firebase

    async def execute(self, matched, client, message):
        await self.firebase.patch(
            path="server/{}".format(message.server.id),
            value={
                "notify_channel_id": message.channel.id
            }
        )
        await client.send_message(
            message.channel,
            "Set notify channel to {}".format(message.channel.name)
        )

    def help(self, client):
        return f"""
**@{client.user} set_notify**

メッセージを送信したチャンネルを通知チャンネルに設定します。
    """
