import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth

import asyncio
import websockets
import json, random, os, sys

async def message(message, websocket, CLIENTS, context):
    return 
    default_channel = context[1]
    channels = context[0]
    print('message')

    messages.append(message)
    print(messages)

async def auth_success(message, websocket, CLIENTS, context):
    return
    print('auth')
    for i in messages:
        print(str(i))
        await websocket.send(str(i))