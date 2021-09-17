import asyncio, WebsJSON, json

async def main(WSHandler, ws):
    print(await ws.ping())
    while True:
        await ws.send(json.dumps({'type':'message', 'message':input('>')}))

async def onConnect(ws):
    await ws.send('{"type":"auth", "token":"abcd1234"}')

h = WebsJSON.WSHandler('ws://2.tcp.ngrok.io:12104', onConnect=onConnect, thread=main)

@h.handle('message')
async def messageHandler(ctx, message, channel, author):
    print(f'{author} -> {channel}: {message}')

@h.handle()
async def defaultHandler(ctx, **kwargs):
    print(kwargs)

h.connect()
