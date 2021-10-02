import utils.pluginUtils as pluginUtils

rplugins = pluginUtils.loadPlugins()

plugins = pluginUtils.pluginDict(rplugins)

handlers = pluginUtils.getHandlers(rplugins)
        
async def handleMessage(message, websocket, CLIENTS, context):
    context += (plugins,)
    if message['type'] in handlers.keys():
        for handler in handlers[message['type']]:
            await handler(message, websocket, CLIENTS, context)

async def handleConnect(websocket, CLIENTS, context):
    context += (plugins,)
    if 'connect' in handlers.keys():
        for handler in handlers['connect']:
            await handler(websocket, CLIENTS, context)

async def handleDisconnect(websocket, CLIENTS, context):
    context += (plugins,)
    if 'disconnect' in handlers.keys():
        for handler in handlers['disconnect']:
            await handler(websocket, CLIENTS, context)