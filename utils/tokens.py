import json

def getTokens(token = None):
    with open('tokens.json') as f:
        if token is None:
            return json.load(f)
        else:
            return json.load(f)[token]