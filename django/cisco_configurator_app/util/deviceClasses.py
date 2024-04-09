import json
class deviceInfo:
    def __init__(self, hostname:str = None, motd:str = None) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(hostname) == str:
            self.hostname = hostname
        else:
            raise TypeError()

        if type(motd) == str:
            self.motd = motd
        else:
            raise TypeError()
        
    def __repr__(self) -> str:
        return "Hostname: " + self.hostname + "\n" + "MOTD: " + self.motd

class interfaces:
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, description:str = None, shutdown:str = None ) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(interface) == str:
            self.interface = interface #FastEthernet0/0
        else:
            raise TypeError()
        if type(ip) == str:
            self.ip = ip
        else:
            raise TypeError()
        if type(sm) == str:
            self.sm = sm
        else:
            raise TypeError()
        if type(description) == str:
            self.description = description
        else:
            raise TypeError()
        if type(shutdown) == str:
            self.shutdown = shutdown
        else:
            raise TypeError()
        
    def __repr__(self) -> str:
        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + self.shutdown

    def toConfig(self) -> list:
        return [self.interface, f' ip address {self.ip} {self.sm}\n', f' description {self.description}\n', f' {self.shutdown}\n']

class StaticRouting:
    def __init__(self, staticRouting:str = "0.0.0.0,0.0.0.0,0.0.0.0;1.1.1.1,1.1.1.1,1.1.1.1" ) -> None:
        self.routes = []
        self.routes_str = None
        self.getRoutes(staticRouting)

    def getRoutes(self, staticRouting:str) -> list:
        if staticRouting:
            routes = staticRouting.split(';')
            for route in routes:
                targetNw, targetSm, nextHop = route.split(',')
                self.routes.append({'targetNw': targetNw, 'targetSm': targetSm, 'nextHop': nextHop})
        return self.routes

    def getString(self) -> str:
        if self.routes_str is None:
            routes_str = []
            for route in self.routes:
                route_str = ','.join([route['targetNw'], route['targetSm'], route['nextHop']])
                routes_str.append(route_str)
            self.routes_str = ';'.join(routes_str)
        return self.routes_str

    def toConfig(self) -> list:
        config = []
        for route in self.routes:
            config.append(f"ip route {route['targetNw']} {route['targetSm']} {route['nextHop']}")
        return config


class ripRouting:
    def __init__(self, ripVersion:str = None, ripSumState:str = None, ripOriginate:str = None, ripNetworks:str = None) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(ripVersion) == str:
            self.ripVersion = ripVersion
        else:
            raise TypeError()

        if type(ripSumState) == str:
            self.ripSumState = ripSumState
        else: 
            raise TypeError()
        
        if type(ripOriginate) == str:
            self.ripOriginate = ripOriginate
        else:
            raise TypeError()
        
        if type(ripNetworks) == str:
            self.ripNetworks = self.getNetworks(ripNetworks)
        else:
            raise TypeError()

    # Teilt den String in die einzelnen Netzwerke auf und speichert sie in einer Liste
    def getNetworks(self, ripNetworks:str) -> list:
        if ripNetworks:
            networks = ripNetworks.split(',')
            return networks
        return []
    
class nat:
    # Teilt den String in die einzelnen Werte auf und speichert sie in einer Liste
    def splitNatPool(self) -> list:
        if ',' in self.natPool:
            accessNw, accessSm = self.natPool.split(',')
            return [accessNw, accessSm]
        else:
            raise ValueError("natPool should contain a ','")
    #Überprüft ob die Eingabe ein String ist und speichert die Werte
    def __init__(self, natInside:str = "defaultInside", natOutside:str = "defaultOutside", natPool:str = "192.168.16.0,0.0.0.255") -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(natInside) == str:
            self.natInside = natInside
        else:
            raise TypeError()

        if type(natOutside) == str:
            self.natOutside = natOutside
        else:
            raise TypeError()
        
        if type(natPool) == str:
            self.natPool = natPool
            self.accessList = self.splitNatPool()
        else:
            raise TypeError()

class dhcp:
    def __init__(self, state:str = "off", dhcpPoolName:str = "pool1", dhcpNetwork:str = "0.0.0.0", dhcpGateway:str = "0.0.0.0", dhcpDNS:str = "0.0.0.0", dhcpPool:str = "0.0.0.0,0.0.0.0" ) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(state) == str:
            self.state = state
        else:
            raise TypeError()

        if type(dhcpPoolName) == str:
            self.dhcpPoolName = dhcpPoolName
        else:
            raise TypeError()
        
        if type(dhcpNetwork) == str:
            self.dhcpNetwork = dhcpNetwork
        else:
            raise TypeError()
        
        if type(dhcpGateway) == str:
            self.dhcpGateway = dhcpGateway
        else:
            raise TypeError()
        
        if type(dhcpDNS) == str:
            self.dhcpDNS = dhcpDNS
        else:
            raise TypeError()
        
        if type(dhcpPool) == str:
            self.dhcpPool = dhcpPool
            self.dhcpPoolList = self.splitDhcpPool()
        else:
            raise TypeError()

    def splitDhcpPool(self):
        # split the dhcpPool string at the comma
        split_pool = self.dhcpPool.split(',')

        # check if the split operation resulted in exactly two elements
        if len(split_pool) != 2:
            raise ValueError("dhcpPool must be two IP addresses separated by a comma")

        return split_pool
    


