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
    
    def __setitem__(self, item, value):
        self.message[item] = value

    def __str__(self):
        return json.dumps(self.message, indent = 4)
    
    def keys(self):
        return self.message.keys()

async def handleLogin(webs, clients, auth, channels, default_channel):

    await webs.send(formatMessage('auth', new_account = False, success = True, username = auth.username))

    out = []

    for ii, i in enumerate(clients):

        if i[0] != auth.token:

            try:

                await i[2].send(formatMessage('join', username = auth.username))
            
            except:
                del clients[ii]

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

async def sendToAll(ws, CLIENTS, message):
    for j, i in enumerate(CLIENTS):
        await i[2].send(message)