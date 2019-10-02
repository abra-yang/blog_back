
class Authmiddle(object):
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,requeset):
        #拦截request
        #print('+++++++')
        response = self.get_response(requeset)
        #print(response.__dict__)
        return response