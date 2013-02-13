__author__ = 'fatih'

class Group():
    """
        Group class to create a runtime instance while adding a new device
    """
    name = None
    config_id = None

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setConfig(self, config):
        self.config_id = config

    def getConfig(self):
        return self.config_id