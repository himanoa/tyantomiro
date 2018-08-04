from re import sub, compile


def get_removed_mention_text(message, client):
    if [user for user in message.mentions if user == client.user]:
        return (sub(r'<.+>\s', '', message.content))


def matcher(responses, message, client):
    compiled_responses = [{**res, **{"pattern": compile(res.get("pattern"))}}
                          for res in responses]

    async def _matcher(message, client):
        if client.user != message.author:
            text = get_removed_mention_text(message, client)
            [await res["responses"].execute()
                for res in compiled_responses
                if res.get("pattern").match(text)]
        return _matcher
