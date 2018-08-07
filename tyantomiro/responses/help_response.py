from .base_response import BaseResponse


class HelpResponse(BaseResponse):

    def __init__(self, responses):
        self.responses = responses

    async def execute(self, pattern, client, message):
        await client.send_message(message.channel, self.create_help(client))

    def create_help(self, client):
        return '''\
{}
'''.format(
    "\n".join(
        [r.help(client) for r in map(lambda x:x["response"], self.responses)]
    )
)

    def help(self, client):
        return ""
