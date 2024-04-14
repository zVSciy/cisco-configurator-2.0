import json

#region Device

class DeviceInfo:
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

class Interface:
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

    def __repr__(self) -> str:
        return json.dumps(self.routes, indent=4)
    
    def toConfig(self) -> list:
        config = []
        for route in self.routes:
            config.append(f"ip route {route['targetNw']} {route['targetSm']} {route['nextHop']}\n")
        config.append("!\n")
        return config

#endregion
#region RIP

class RipRouting:
    def __init__(self, ripVersion:str = None, ripSumState:bool = None, ripOriginate:bool = None, ripNetworks:str = None) -> None:
        #Überprüft ob die Eingabe ein String ist und speichert die Werte
        if type(ripVersion) == str:
            self.ripVersion = ripVersion
        else:
            raise TypeError()

        if type(ripSumState) == bool:
            self.ripSumState = "no-auto summary\n" if ripSumState else ''
        else: 
            raise TypeError()
        
        if type(ripOriginate) == bool:
            self.ripOriginate = "default-information originate\n" if ripOriginate else ''
        else:
            raise TypeError()
        
        if type(ripNetworks) == str:
            self.ripNetworks = self.getNetworks(ripNetworks)
        else:
            raise TypeError()

    # Teilt den String in die einzelnen Netzwerke auf und speichert sie in einer Liste
    def getNetworks(self, ripNetworks:str) -> list:
        return ripNetworks.split(';')

    def __repr__(self) -> str:
        return "RIP Version: " + self.ripVersion + "\n" + "Auto Summary: " + self.ripSumState + "\n" + "Default Information Originate: " + self.ripOriginate + "\n" + "Networks: " + ', '.join(self.ripNetworks) + "\n"
    
    def toConfig(self) -> list:
        config = []
        config.append("router rip\n")
        config.append(f" version {self.ripVersion}\n")
        if self.ripSumState:
            config.append(f" {self.ripSumState}")
        if self.ripOriginate:
            config.append(f" {self.ripOriginate}")
        for network in self.ripNetworks:
            config.append(f" network {network}\n")
        config.append("!\n")
        return config

#endregion
#region DHCP

class DHCP:
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
            self.areas = []
            self.getAreas(dhcpExcludedAreas)
        else:
            raise TypeError()
        
        if type(dhcpPoolName) == str:
            self.dhcpPoolName = dhcpPoolName
        else:
            raise TypeError()
        
    def getAreas(self, dhcpExcludeAreas:str) -> list:
        if dhcpExcludeAreas:
            areas = dhcpExcludeAreas.split(';')
            for area in areas:
                AreaFromIP, AreaToIP = area.split(',')
                self.areas.append({'AreaFromIP': AreaFromIP, 'AreaToIP': AreaToIP})
        return self.areas
    
    def __repr__(self) -> str:
        return "Network IP: " + self.dhcpNetworkIP + "\n" + "Network Subnet Mask: " + self.dhcpNetworkSM + "\n" + "Gateway: " + self.dhcpGateway + "\n" + "DNS: " + self.dhcpDNS + "\n" + "Excluded Areas: " + ', '.join(self.dhcpExcludedAreas) + "\n" + "Pool Name: " + self.dhcpPoolName + "\n"
    
    def toConfig(self) -> list:
        config = []
        for area in self.areas:
            config.append(f"ip dhcp excluded-address {area['AreaFromIP']} {area['AreaToIP']}\n")
        config.append("!\n")
        config.append(f"ip dhcp pool {self.dhcpPoolName}\n")
        config.append(f"   network {self.dhcpNetworkIP} {self.dhcpNetworkSM}\n")
        config.append(f"   default-router {self.dhcpGateway}\n")
        config.append(f"   dns-server {self.dhcpDNS}\n")
        config.append("!\n")
        return config

#endregion
#region NAT

class NAT:
    def __init__(self, interfaceName:str = None, accessListName:str = None) -> None:
        # Permit Any und 0.0.0.0 0.0.0.255
        if type(interfaceName) == str:
            self.interface = interfaceName
        else:
            raise TypeError()
        if type(accessListName) == str:
            self.accessList = accessListName
        else:
            raise TypeError()
    def __repr__(self) -> str:
        return "Interface: " + self.interface + "\n" + "Access List: " + self.accessList + "\n"
    
    def toConfig(self) -> list:
        config = []
        config.append(f"ip nat inside source list {self.accessList} interface {self.interface} overload\n" + "!\n")
        return config

#endregion
#region ACL

class ACLStandard:
    def __init__(self, accessList:str = None) -> None:
        if type(accessList) == str:
            self.ACLs = []
            self.getACLs(accessList)
        else:
            raise TypeError()  
        
    #"ACLID,deny|permit,IP,SM;ACLID,deny|permit,IP,SM;ACLID,IP,SM"
    def getACLs(self, accessList:str) -> list:
        if accessList:
            ACLs = accessList.split(';')
            for ACL in ACLs:
                if(len(ACL.split(',')) == 3):
                    id, permitDeny, ip = ACL.split(',')
                    self.ACLs.append({'id': id, 'permitDeny': permitDeny, 'ip': ip})
                elif (len(ACL.split(',')) == 4):
                    id, permitDeny, ip, sm = ACL.split(',')
                    self.ACLs.append({'id': id,'permitDeny': permitDeny, 'ip': ip, 'sm': sm})
        return self.ACLs                                                                   

    def __repr__(self) -> str:
        return json.dumps(self.ACL, indent=4)
    
    def toConfig(self) -> list:
        config = []
        for acl in self.ACLs:
            if len(acl) == 3:
                config.append(f"access-list {acl['id']} {acl['permitDeny']} {acl['ip']}\n")
            elif len(acl) == 4:
                config.append(f"access-list {acl['id']} {acl['permitDeny']} {acl['ip']} {acl['sm']}\n")
        config.append("!\n")
        return config
    
#region OSPF
 
class OSPF:
    def __init__(self, ospfProcess:str = None, ospfRouterID:str = None, ospfNetworks:str = None) -> None:
        if type(ospfProcess) == str:
            self.ospfProcess = ospfProcess
        else:
            raise TypeError()
        
        if type(ospfRouterID) == str:
            self.ospfRouterID = ospfRouterID
        else:
            raise TypeError()
        
        if type(ospfNetworks) == str:
            self.ospfNetworks = self.getNetworks(ospfNetworks)
        else:
            raise TypeError()

#endregion