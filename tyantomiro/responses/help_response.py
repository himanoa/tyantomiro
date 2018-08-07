from .base_response import BaseResponse

class HelpResponse(BaseResponse):
    def __init__(self, responses):
        self.responses = responses

    async def execute(self, pattern, message, client):
        help = '''\
        {}
        '''.format("\n".join([r.help(client) for r in self.responses]))
        await client.send_message(message.channel, help)

    def help(self, client):
        return ""
