"Default handlers, and example plugin."

import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth

import asyncio
import websockets
import json, random, os, sys

async def auth(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]
    auth = Auth(websocket, message)

    if auth.isvalid:
        CLIENTS.append((auth.token, auth.username, websocket))
        websocket.id = len(CLIENTS)
        websocket.auth = auth

        await handleLogin(websocket, CLIENTS, auth, channels, default_channel)
        print(f"+ {auth.username} has been authorized.")
        message['type'] = 'auth_success'
        await context[2].handleMessage(message, websocket, CLIENTS, context)

    else:
        await websocket.send(formatMessage('auth', new_account = False, success = False))
        await websocket.close(1011, 'Invalid Token')
        message['type'] = 'auth_fail'
        await context[2].handleMessage(message, websocket, CLIENTS, context)
        print(f"* {auth.username} has failed to be authorized.")
        return 'Exit'

async def message(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]

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

async def direct_message(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]

    for i in CLIENTS:
        if i[1] == message['recipient']:
            await i[2].send(formatMessage('direct_message', author = websocket.auth.username, message = message['message']))

async def typing(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]

    for i in CLIENTS:
        if i[2] != websocket:
            await i[2].send(formatMessage('typing', username = i[1]))

async def typing(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]

    await websocket.send(json.dumps(await getUserList(websocket, CLIENTS, websocket.auth)))