from src.model.Commands import Commands

__author__ = 'fatih'


class Request(dict):
    """
        Request object class to generate a new request
        "enable":true,
        "configure":false,
        "commands":[
            {
                "command":"showa dot11 bssid"
            }
        ]
    """
    enable = True
    configure = False
    commands = Commands()

    def setEnable(self, status):
        self.enable = status

    def getEnable(self):
        return self.enable

    def setConfigure(self, status):
        self.configure = status

    def getConfigure(self):
        return self.configure

    def setCommands(self, commands):
        self.commands = commands

    def getCommands(self):
        return self.commands

    def addCommand(self, command):
        self.commands.append(command)