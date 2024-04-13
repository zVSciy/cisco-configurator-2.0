import json

#MARK: DeviceInfo

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

#MARK: Interfaces

class interfaces:
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, ipNatInside:bool = None, ipNatOutside:bool = None, description:str = None, shutdown:str = None ) -> None:
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
        if type(ipNatInside) == bool:
            self.ipNatInside = "\nip nat inside" if ipNatInside else ''
        else:
            raise TypeError()
        if type(ipNatOutside) == bool:
            self.ipNatOutside = "\nip nat outside" if ipNatOutside else ''
        else:
            raise TypeError()
        
    def __repr__(self) -> str:
        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + self.shutdown + self.ipNatInside + self.ipNatOutside

    def toConfig(self) -> list:
        return [self.interface + "\n", f' ip address {self.ip} {self.sm}\n', f' description {self.description}\n', f' {self.shutdown}\n', f'{self.ipNatInside}', f'{self.ipNatOutside}']
    

#MARK: Static Routing

class StaticRoute:
    def __init__(self, staticRouting:str = None ) -> None:
        self.routes = []
        self.getRoutes(staticRouting)

    def getRoutes(self, staticRouting:str) -> list:
        if staticRouting:
            routes = staticRouting.split(';')
            for route in routes:
                targetNw, targetSm, nextHop = route.split(',')
                self.routes.append({'targetNw': targetNw, 'targetSm': targetSm, 'nextHop': nextHop})
        return self.routes

    def toConfig(self) -> list:
        config = []
        for route in self.routes:
            config.append(f"ip route {route['targetNw']} {route['targetSm']} {route['nextHop']}\n")
        return config

#MARK: RIP

class ripRouting:
    def __init__(self, ripVersion:str = None, ripSumState:bool = None, ripOriginate:bool = None, ripNetworks:str = None) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(ripVersion) == str:
            self.ripVersion = ripVersion
        else:
            raise TypeError()

        if type(ripSumState) == bool:
            self.ripSumState = "no-auto summary" if ripSumState else None
        else: 
            raise TypeError()
        
        if type(ripOriginate) == bool:
            self.ripOriginate = "default-information originate" if ripOriginate else None
        else:
            raise TypeError()
        
        if type(ripNetworks) == str:
            self.ripNetworks = self.getNetworks(ripNetworks)
        else:
            raise TypeError()

    # Teilt den String in die einzelnen Netzwerke auf und speichert sie in einer Liste
    def getNetworks(self, ripNetworks:str) -> list:
        return ripNetworks.split(';')

    def toConfig(self) -> list:
        config = []
        config.append("router rip\n")
        config.append(f" version {self.ripVersion}\n")
        if self.ripSumState:
            config.append(f" {self.ripSumState}\n")
        if self.ripOriginate:
            config.append(f" {self.ripOriginate}\n")
        for network in self.ripNetworks:
            config.append(f" network {network}\n")
        return config

#MARK: DHCP

class dhcp:
    def __init__(self, dhcpNetwork:str = None, dhcpGateway:str = None, dhcpDNS:str = None, dhcpPool:str = None) -> None:
        if type(dhcpNetwork) == str:
            self.dhcpNetwork = dhcpNetwork.split(',')
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
            self.dhcpPool = dhcpPool.split(',')
        else:
            raise TypeError()

    def toConfig(self) -> list:
        config = []
        config.append(f"ip dhcp excluded-address {', '.join(self.dhcpPool)}\n")
        config.append("ip dhcp pool defaultPool\n")
        config.append(f"network {', '.join(self.dhcpNetwork)}\n")
        config.append(f"default-router {self.dhcpGateway}\n")
        config.append(f"dns-server {self.dhcpDNS}\n")
        return config

#MARK: NAT

class nat:
    def __init__(self, natPool:str = "192.168.16.0,0.0.0.255", interfaceName:str = None) -> None:
        if type(natPool) == str:
            self.natPool = natPool.split(',')
        else:
            raise TypeError()
        if type(interfaceName) == str:
            self.interface = interfaceName
        else:
            raise TypeError()

    def toConfig(self) -> list:
        config = []
        config.append(f"ip nat inside source list 1 interface {self.interface} overload\n")
        config.append(f"access list 1 permit {', '.join(self.natPool)}\n")
        return config
        

    


