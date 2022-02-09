
from serilizer.json import JSONSerilizable

class Message():
    def __init__ (self, message ):
        self.message = message

    def __iter__(self):
        yield 'message', self.message

class Response(JSONSerilizable):

    ERROR = "error"

    def __init__ (self, data , status = 'ok'):
        self.status = status
        self.data = data

    def toJSON(self):
        ret = dict(self.data)
        ret.update( { 'status' :  str(self.status) } )
        return ret

