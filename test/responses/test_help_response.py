import unittest
import asyncio

from tyantomiro.responses.help_response import HelpResponse
from tyantomiro.responses.base_response import BaseResponse


class StubMessage:
    def __init__(self):
        self.channel = None


class StubClient:
    def __init__(self):
        self.client = None

    async def send_message(self, channel, help):
        pass


class TestHelpResponse(unittest.TestCase):

    def test_should_be_return_empty_string(self):
        expected = '\n'
        self.assertEqual(HelpResponse([]).create_help(StubClient()), expected)

    def test_should_be_return_help_response(self):
        expected = "foobar\n"

        class StubClient:
            def __init__(self):
                self.user = 'test#1234'

        class StubResponse(BaseResponse):
            def help(self, client):
                return "foobar"

        self.assertEqual(
            HelpResponse([{"response": StubResponse(), 'pattern': r'^s'}]).create_help(StubClient()), expected
        )

    def test_should_be_run_execute(self):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        async def run_test():
            expected = ''
            await HelpResponse([]).execute(
                '',
                StubClient(),
                StubMessage()
            ), expected

        coro = asyncio.coroutine(run_test)
        event_loop.run_until_complete(coro())
        event_loop.close()


if __name__ == '__main__':
    unittest.main()
