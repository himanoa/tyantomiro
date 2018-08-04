class BaseResponse:
    async def execute(self, matched, client, message):
        raise NotImplementedError

    async def help(self, client, message):
        raise NotImplementedError
