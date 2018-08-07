from .base_response import BaseResponse

class HelpResponse(BaseResponse):

    def __init__(self, responses):
        self.responses = responses

    async def execute(self, pattern, message, client):
        await client.send_message(message.channel, self.create_help(client))

    def create_help(self, client):
        return '''\
{}
'''.format("\n".join([r.help(client) for r in self.responses]))

    def help(self, client):
        return ""
