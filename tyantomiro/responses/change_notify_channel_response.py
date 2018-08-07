from .base_response import BaseResponse


class ChangeNotifyChannelResponse(BaseResponse):

    def __init__(self, firebase):
        self.firebase = firebase

    async def execute(self, matched, client, message):
        self.firebase.put(path="server/{}".format(message.server.id))

    def help(self, message):
        pass
