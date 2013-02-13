__author__ = 'fatih'


class Response(dict):
    """
        Response is a class to handle the CI response
    """
    status = None
    message = None

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setMessage(self, message):
        self.message = message

    def getMessage(self):
        return self.message