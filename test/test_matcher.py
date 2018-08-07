import unittest
from types import FunctionType

from tyantomiro.matcher import get_removed_mention_text, create_matcher


class StubClient():
    def __init__(self, user):
        self.user = user


class TestGetRemovedMentionText(unittest.TestCase):

    def test_should_be_input_string(self):
        class StubMessage:
            def __init__(self, content):
                self.content = content
                self.mentions = []
        expected_message = "Hogefuga"
        actual = get_removed_mention_text(StubMessage(expected_message),
                                          StubClient(None))
        self.assertEqual(expected_message, actual)

    def test_should_be_removed_mention_parameter(self):
        class StubMessage:
            def __init__(self, content, users):
                self.content = content
                self.mentions = users
        expected_message = "<asdasuahsj_paramete> "
        actual = get_removed_mention_text(StubMessage(expected_message,
                                                      ['foobar']),
                                          StubClient('foobar'))
        self.assertNotEqual(expected_message, actual)


class TestCreateMatcher(unittest.TestCase):

    def test_should_be_return_matcher_function(self):
        responses = [
            {"pattern": r'^ping', "response": None}
        ]
        self.assertIsInstance(create_matcher(responses), FunctionType)


if __name__ == '__main__':
    unittest.main()
