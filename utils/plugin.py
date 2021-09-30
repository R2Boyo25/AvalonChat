import utils.pluginUtils as pluginUtils

plugins = pluginUtils.loadPlugins()

handlers = pluginUtils.getHandlers(plugins)
        
async def handleMessage(message, websocket, CLIENTS, context):
    if message['type'] in handlers.keys():
        for handler in handlers[message['type']]:
            await handler(message, websocket, CLIENTS, context)

async def handleConnect(websocket, CLIENTS, context):
    if 'connect' in handlers.keys():
        for handler in handlers['connect']:
            await handler(websocket, CLIENTS, context)

async def handleDisconnect(websocket, CLIENTS, context):
    if 'disconnect' in handlers.keys():
        for handler in handlers['disconnect']:
            await handler(websocket, CLIENTS, context)