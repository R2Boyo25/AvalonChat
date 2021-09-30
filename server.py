import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth
import utils.plugin as plugins

import asyncio
import websockets
import json, random, os, sys

try:
    port = sys.argv[1]
except:
    port = 8090

#os.system('clear')

with open('channels.json', 'r') as f:
    channels = json.load(f)

default_channel = 'general'

CLIENTS = []

async def handleConnection(websocket, path):
    global channels

    if await plugins.handleConnect(websocket, CLIENTS, (channels, default_channel)) == 'Exit':
        return

    async for message in websocket:
        try:
            await updateChannelList()
            await delDuplicateWebsockets()
            message = Message(message)

            if await plugins.handleMessage(message, websocket, CLIENTS, (channels, default_channel)) == 'Exit':
                return

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
    
    if await plugins.handleDisconnect(websocket, CLIENTS, (channels, default_channel)) == 'Exit':
        return

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
                try:
                    del CLIENTS[j]
                except:
                    pass


async def main():
    global channels
    print('Server Ready')
    async with websockets.serve(handleConnection, "0.0.0.0", port, ping_timeout=None, ping_interval=None):
        try:
            await asyncio.Future()  # run forever
        except:
            pass


asyncio.run(main())