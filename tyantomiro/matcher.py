from re import sub, compile


def get_removed_mention_text(message, client):
    if [user for user in message.mentions if user == client.user]:
        return (sub(r'<.+>\s', '', message.content))


def create_matcher(responses):
    compiled_responses = [{**res, **{"pattern": compile(res["pattern"])}}
                          for res in responses]

    async def _matcher(message, client):
        if client.user != message.author:
            text = get_removed_mention_text(message, client)
            [await res["response"].execute(res.get("pattern").match(text),
                                           client, message)
                for res in compiled_responses
                if res.get("pattern").match(text)]
    return _matcher
