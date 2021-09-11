import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth

import asyncio
import websockets
import json, random

with open('channels.json', 'r') as f:
    channels = json.load(f)

default_channel = 'general'

CLIENTS = []

async def handleMessage(websocket, path):

    async for message in websocket:
        try:
            message = Message(message)

            print(message)

            for i in CLIENTS:
                for j, ii in enumerate(CLIENTS):
                    if i[0] == ii[0] and i != ii:
                        del CLIENTS[j]

            if message['type'] == 'auth':
                auth = Auth(websocket, message)

                if auth.isvalid:
                    CLIENTS.append((auth.token, auth.username, websocket))
                    websocket.id = len(CLIENTS)
                    websocket.auth = auth

                    await handleLogin(websocket, CLIENTS, auth, channels, default_channel)

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
                    for i in CLIENTS:
                        if i[2] != websocket:
                            await i[2].send(formatMessage('message', channel = channel, author = websocket.auth.username, message = message['message']))

                except:
                    channel = default_channel
                    for i in CLIENTS:
                        if i[2] != websocket:
                            await i[2].send(formatMessage('message', channel = channel, author = websocket.auth.username, message = message['message']))

        except asyncio.exceptions.CancelledError:
            for j, i in enumerate(CLIENTS):
                if i[2] == websocket:
                    for ii in CLIENTS:
                        if ii != i:
                            await ii[2].send(formatMessage('leave', username = i[1]))
                    del CLIENTS[j]


    for j, i in enumerate(CLIENTS):
        if i[2] == websocket:
            for ii in CLIENTS:
                if ii != i:
                    await ii[2].send(formatMessage('leave', username = i[1]))
            del CLIENTS[j]

async def main():
    global channels
    async with websockets.serve(handleMessage, "0.0.0.0", 8090):
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
        await asyncio.Future()  # run forever

asyncio.run(main())