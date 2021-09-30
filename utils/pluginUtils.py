from importlib import import_module
import os

def getAttrs(plugin):
    filteredattrs = []
    for attr in dir(plugin):
        if not attr.startswith('_'):
            filteredattrs.append(attr)
    
    return filteredattrs

def loadPlugins():
    plugins = []

    plugindir = "plugins"
    pluginfiles = os.listdir(plugindir)
    pluginfiles = [i for i in pluginfiles if os.path.isfile('plugins/' + i)]
    for pluginfile in pluginfiles:
        plugin = import_module("plugins."+pluginfile.split('.')[0])
        plugins.append(plugin)
    
    return plugins

def getHandlers(plugins):
    handlers = {}
    for plugin in plugins:
        for handlername in getAttrs(plugin):
            handler = getattr(plugin, handlername)
            if not handlername in handlers.keys():
                handlers[handlername] = []
            
            handlers[handlername].append(handler)
    
    return handlers

