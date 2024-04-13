import json

#region Device

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
        return "Hostname: " + self.hostname + "\n" + "MOTD: " + self.motd + "!\n"
    
#endregion
#region Interfaces

class interfaces:
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, ipNatInside:bool = None, ipNatOutside:bool = None, description:str = "Default", shutdown:bool = None ) -> None:
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
        if type(shutdown) == bool:
            self.shutdown = "no shutdown\n" if shutdown else "shutdown\n"
        else:
            raise TypeError()
        if type(ipNatInside) == bool:
            self.ipNatInside = "ip nat inside\n" if ipNatInside else ''
        else:
            raise TypeError()
        if type(ipNatOutside) == bool:
            self.ipNatOutside = "ip nat outside\n" if ipNatOutside else ''
        else:
            raise TypeError()
        
    def __repr__(self) -> str:
        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + self.shutdown + "\n" + self.ipNatInside + self.ipNatOutside 

    def toConfig(self) -> list:
        return [self.interface + "\n", f' ip address {self.ip} {self.sm}\n', f' description {self.description}\n', f' {self.shutdown}', f' {self.ipNatInside}', f'{self.ipNatOutside}' + "!\n"]

# Erstellen Sie eine Instanz der Klasse
interface_instance = interfaces(interface="FastEthernet0/0", ip="192.168.1.1", sm="255.255.255.0", description="Main Interface", shutdown=True, ipNatInside=True, ipNatOutside=False)
interface_instance = interfaces(interface="FastEthernet0/1", ip="192.168.1.2", sm="255.255.255.0", description="Main Interface2", shutdown=False, ipNatInside=False, ipNatOutside=True)

config = interface_instance.toConfig()
print(config)

#endregion
#region StaticRoute

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
            config.append(f"ip route {route['targetNw']} {route['targetSm']} {route['nextHop']}\n" + "!\n")
        return config

#endregion
#region RIP

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
        config.append("!\n")
        return config

#endregion
#region DHCP

class dhcp:
    def __init__(self, dhcpNetworkIP:str = None,dhcpNetworkSM:str = None, dhcpGateway:str = None, dhcpDNS:str = None, dhcpExcludedAreas:str = None, dhcpPoolName:str = None) -> None:
        
        if type(dhcpNetworkIP) == str:
            self.dhcpNetworkIP = dhcpNetworkIP
        else:
            raise TypeError()
        
        if type(dhcpNetworkSM) == str:
            self.dhcpNetworkSM = dhcpNetworkSM
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
        
        if type(dhcpExcludedAreas) == str:
            self.dhcpExcludedAreas = dhcpExcludedAreas.split(',')
        else:
            raise TypeError()
        if type(dhcpPoolName) == str:
            self.dhcpPoolName = dhcpPoolName
        else:
            raise TypeError()
    def __repr__(self) -> str:
        return "Network IP: " + self.dhcpNetworkIP + "\n" + "Network Subnet Mask: " + self.dhcpNetworkSM + "\n" + "Gateway: " + self.dhcpGateway + "\n" + "DNS: " + self.dhcpDNS + "\n" + "Excluded Areas: " + ', '.join(self.dhcpExcludedAreas) + "\n" + "Pool Name: " + self.dhcpPoolName + "\n"
    
    def toConfig(self) -> list:
        config = []
        config.append(f"ip dhcp excluded-address {', '.join(self.dhcpExcludedAreas)}\n" + "!\n")
        config.append(f"ip dhcp pool {self.dhcpPoolName}\n")
        config.append(f"   network {self.dhcpNetworkIP} {self.dhcpNetworkSM}\n")
        config.append(f"   default-router {self.dhcpGateway}\n")
        config.append(f"   dns-server {self.dhcpDNS}\n")
        config.append("!\n")
        return config

#endregion
#region NAT

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
        config.append(f"ip nat inside source list 1 interface {self.interface} overload\n" + "!\n")
        config.append(f"access list 1 permit {', '.join(self.natPool)}\n" + "!\n")
        config.append("!\n")
        return config

#endregion



