# coding=utf-8
__author__ = 'fatih'


class Response(dict):
    """
        Response is a class to handle the CI response
    """
    status = None
    message = None

    def setStatus(self, status):
        """

        :param status:
        """
        self.status = status

    def getStatus(self):
        """

        :return:
        """
        return self.status

    def setMessage(self, message):
        """

        :param message:
        """
        self.message = message

    def getMessage(self):
        """

        :return:
        """
        return self.message