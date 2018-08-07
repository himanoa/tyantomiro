from .base_response import BaseResponse


class PongResponse(BaseResponse):
    async def execute(self, matched, client, message):
        await client.send_message(message.channel, "PONG")

    def help(self, client):
        return f"""
**@{client.user} ping**

PONGと応答します。
    """
