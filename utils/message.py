import json

def formatMessage(mtype, **kwargs):
    out = {"type":mtype}
    for i in kwargs.keys():
        out[i] = kwargs[i]
    return json.dumps(out)


class Message:
    def __init__(self, message):
        self.message = json.loads(message)
    
    def __getitem__(self, item):
        return self.message[item]

    def __str__(self):
        return json.dumps(self.message)

async def handleLogin(webs, clients, auth, channels, default_channel):

    await webs.send(formatMessage('auth', new_account = False, success = True, username = auth.username))

    out = []

    for i in clients:

        if i[0] != auth.token:

            await i[2].send(formatMessage('join', username = auth.username))

            out.append(i[1])

    await webs.send(formatMessage('user_list', users = out))

    await webs.send(formatMessage('channel_list', channels = channels))

    await webs.send(formatMessage('default_channel', channel = default_channel))

async def getUserList(webs, clients, auth):
    out = []

    for i in clients:

        if i[0] != auth.token:

            out.append(i[1])

    await webs.send(
        json.dumps(
            {
                "type" : "user_list",
                "users": out
            }
        )
    )