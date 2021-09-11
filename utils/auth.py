from utils.tokens import getTokens

class Auth:
    def __init__(self, webs, message):
        self.message = message

    @property
    def token(self):
        return self.message['token']
    
    @property
    def username(self):
        return getTokens(self.message['token'])

    @property
    def isvalid(self):
        try:
            getTokens(self.message['token'])
            return True
        except:
            return False