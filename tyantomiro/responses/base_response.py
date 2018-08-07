class BaseResponse:
    async def execute(self, matched, client, message):
        raise NotImplementedError

    def help(self, client):
        raise NotImplementedError
