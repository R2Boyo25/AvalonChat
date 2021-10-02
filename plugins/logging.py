import utils.tokens as tokens
from utils.message import *
from utils.auth import Auth

import asyncio
import websockets
import json, random, os, sys

messages = []

async def message(message, websocket, CLIENTS, context):
    default_channel = context[1]
    channels = context[0]
    
    channel = message['channel'] if 'channel' in message.keys() else default_channel

    messages.append(formatMessage('message', channel = channel, author = websocket.auth.username, message = message['message']))

async def auth_success(message, websocket, CLIENTS, context):
    for message in messages:
        await websocket.send(message)