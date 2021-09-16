import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth

import asyncio
import websockets
import json, random, os, sys

try:
    port = sys.argv[1]
except:
    port = 8090

os.system('clear')

with open('channels.json', 'r') as f:
    channels = json.load(f)

default_channel = 'general'

CLIENTS = []

async def handleMessage(websocket, path):
    global channels

    async for message in websocket:
        try:
            await updateChannelList()
            await delDuplicateWebsockets()
            message = Message(message)

            if message['type'] == 'auth':
                auth = Auth(websocket, message)

                if auth.isvalid:
                    CLIENTS.append((auth.token, auth.username, websocket))
                    websocket.id = len(CLIENTS)
                    websocket.auth = auth

                    await handleLogin(websocket, CLIENTS, auth, channels, default_channel)
                    print(f"+ {auth.username} has been authorized.")

                else:
                    await websocket.send(formatMessage('auth', new_account = False, success = False))
                    await websocket.close(1011, 'Invalid Token')
                    return
            
            elif message['type'] == 'user_list':
                await websocket.send(json.dumps(await getUserList(websocket, CLIENTS, websocket.auth)))
            
            elif message['type'] == 'typing':
                for i in CLIENTS:
                    if i[2] != websocket:
                        await i[2].send(formatMessage('typing', username = i[1]))
            
            elif message['type'] == 'direct_message':
                for i in CLIENTS:
                    if i[1] == message['recipient']:
                        await i[2].send(formatMessage('direct_message', author = websocket.auth.username, message = message['message']))

            elif message['type'] == 'message':
                try:
                    channel = message['channel']
                    for ii, i in enumerate(CLIENTS):
                        if i[2] != websocket:
                            try:
                                await i[2].send(formatMessage('message', channel = channel, author = websocket.auth.username, message = message['message']))
                            except:
                                del CLIENTS[ii]
                            print(f"{channel} -> {i[1]}: {message['message']}")

                except:
                    channel = default_channel
                    for ii, i in enumerate(CLIENTS):
                        if i[2] != websocket:
                            try:
                                await i[2].send(formatMessage('message', channel = channel, author = websocket.auth.username, message = message['message']))
                            except:
                                del CLIENTS[ii]
                            print(f"{channel} -> {i[1]}: {message['message']}")

        except asyncio.exceptions.CancelledError:
            for j, i in enumerate(CLIENTS):
                if i[2] == websocket:
                    for iii, ii in enumerate(CLIENTS):
                        if ii != i:
                            try:
                                await ii[2].send(formatMessage('leave', username = i[1]))
                            except:
                                del CLIENTS[iii]
                    del CLIENTS[j]


    for j, i in enumerate(CLIENTS):
        if i[2] == websocket:
            print(f"- {i[1]} has left")
            for iii, ii in enumerate(CLIENTS):
                if ii != i:
                    try:
                        await ii[2].send(formatMessage('leave', username = i[1]))
                    except:
                        del CLIENTS[iii]
            del CLIENTS[j]

async def updateChannelList():
    global channels
    ochannel = channels
    with open('channels.json', 'r') as f:
        channels = json.load(f)
    if len(ochannel) != len(channels):
        for i in ochannel:
            if i not in channels:
                for ii in CLIENTS:
                    await ii[2].send('channel_delete', channel = i)
        for i in channel:
            if i not in ochannel:
                for ii in CLIENTS:
                    await ii[2].send('channel_create', channel = i)

async def delDuplicateWebsockets():
    for i in CLIENTS:
        for j, ii in enumerate(CLIENTS):
            if i[0] == ii[0] and i != ii:
                try:
                    await i[2].close()
                except:
                    pass
                del CLIENTS[j]


async def main():
    global channels
    print('Server Ready')
    async with websockets.serve(handleMessage, "0.0.0.0", port, ping_timeout=None):
        try:
            await asyncio.Future()  # run forever
        except:
            pass


asyncio.run(main())