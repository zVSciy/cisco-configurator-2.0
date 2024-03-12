import json
class deviceInfo:
    def __init__(self, hostname:str = "DefaultHostname", motd:str = "Welcome") -> None:
        if type(hostname) == str:
            self.hostname = hostname
        else:
            raise ValueError()

        if type(motd) == str:
            self.motd = motd
        else:
            raise ValueError()
        
    def __repr__(self) -> str:
        return "Hostname: " + self.hostname + "\n" + "MOTD: " + self.motd