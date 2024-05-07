import json

#region Device

# Define a class to store device information
class DeviceInfo:
    # Initialize the class with hostname and motd (Message of the Day)
    def __init__(self, hostname:str = None, motd:str = "Cisco Troll") -> None:
        # Check if the hostname is a string and store it
        if type(hostname) == str:
            self.hostname = hostname
        else:
            # Raise a TypeError if the hostname is not a string
            raise TypeError()

        # Check if the motd is a string and store it
        if type(motd) == str:
            self.motd = motd
        else:
            # Raise a TypeError if the motd is not a string
            raise TypeError()
        
    # Define the string representation of the class
    def __repr__(self) -> str:
        return "Hostname: " + self.hostname + "\n" + "MOTD: " + self.motd + "!\n"
    
    # Convert the device information to a configuration list
    def toConfig(self) -> list:
        return [f"hostname {self.hostname}\n", "!\n" f"banner motd ^C{self.motd}^C\n", "!\n"]
#endregion
#region Interfaces

# Define a class to store interface information
class Interface:
    # Initialize the class with various parameters
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, ipNatInside:bool = None, ipNatOutside:bool = None, description:str = "Default", shutdown:bool = None ) -> None:
        # Check if the interface is a string and store it
        if type(interface) == str:
            self.interface = interface
        else:
            raise TypeError()

        # Check if the ip is a string and store it, also validate if IP is set to DHCP and subnet mask is provided
        if type(ip) == str:
            self.ip = ip
            if ip.lower() == "dhcp" and sm != '':
                raise ValueError("Subnet mask should not be provided when IP is set to DHCP")
        else:
            raise TypeError()

        # Check if the subnet mask is a string or None and store it
        if type(sm) == str or sm is None:
            self.sm = sm
        else:
            raise TypeError()

        # Check if the description is a string and store it
        if type(description) == str:
            self.description = description
        else:
            raise TypeError()

        # Check if the shutdown status is a boolean and store it, convert it to a string representation
        if type(shutdown) == bool:
            self.shutdown = shutdown
        else:
            raise TypeError()

        # Check if the NAT inside status is a boolean and store it
        if type(ipNatInside) == bool:
            self.ipNatInside = ipNatInside
        else:
            raise TypeError()

        # Check if the NAT outside status is a boolean and store it
        if type(ipNatOutside) == bool:
            self.ipNatOutside = ipNatOutside
        else:
            raise TypeError()

    # Define the string representation of the class
    def __repr__(self) -> str:
        natInside = "ip nat inside\n" if self.ipNatInside else ''
        natOutside = "ip nat outside\n" if self.ipNatOutside else ''
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"

        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + shutdown + "\n" + natInside + natOutside 

    # Convert the interface information to a configuration list
    def toConfig(self) -> list:
        natInside = "ip nat inside\n" if self.ipNatInside else ''
        natOutside = "ip nat outside\n" if self.ipNatOutside else ''
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"
        ipConfig = f' ip address {self.ip} {self.sm}\n' if self.ip.lower() != "dhcp" else ' ip address dhcp\n'

            
        return ["interface " + self.interface + "\n", ipConfig, f' description {self.description}\n', f' {shutdown}', f' {natInside}', f'{natOutside}' + "!\n"]

#endregion
#region StaticRoute

# Define a class to manage static routing configurations
class StaticRoute:
    # Initialize the class with an optional string of static routes
    def __init__(self, staticRouting:str = None ) -> None:
        # Initialize an empty list to store the routes
        self.routes = []
        # If a string of static routes is provided, parse and store the routes
        self.getRoutes(staticRouting)

    # Parse a string of static routes and store them in the routes list
    def getRoutes(self, staticRouting:str) -> list:
        if staticRouting:
            routes = staticRouting.split(';')
            for route in routes:
                if route:
                    targetNw, targetSm, nextHop = route.split(',')
                    self.routes.append({'targetNw': targetNw, 'targetSm': targetSm, 'nextHop': nextHop})
        return self.routes

    # Define the string representation of the class as a JSON string of the routes
    def __repr__(self) -> str:
        return json.dumps(self.routes, indent=4)
    
    # Convert the stored static routes to a list of configuration commands
    def toConfig(self) -> list:
        config = []
        for route in self.routes:
            config.append(f"ip route {route['targetNw']} {route['targetSm']} {route['nextHop']}\n")
        config.append("!\n")
        return config

#endregion
#region RIP

# Define a class to manage RIP routing configurations
class RipRouting:
    # Initialize the class with various parameters
    def __init__(self, ripVersion:str = None, ripSumState:bool = None, ripOriginate:bool = None, ripNetworks:str = None) -> None:
        # Check if the ripVersion is a string and store it
        if type(ripVersion) == str:
            self.ripVersion = ripVersion
        else:
            raise TypeError()

        # Check if the ripSumState is a boolean and store it
        if type(ripSumState) == bool:
            self.ripSumState = ripSumState
        else: 
            raise TypeError()
        
        # Check if the ripOriginate is a boolean and store it
        if type(ripOriginate) == bool:
            self.ripOriginate = ripOriginate
        else:
            raise TypeError()
        
        # Check if the ripNetworks is a string and store it
        if type(ripNetworks) == str:
            self.ripNetworks = self.getNetworks(ripNetworks)
        else:
            raise TypeError()

    # Split the ripNetworks string into individual networks and store them in a list
    def getNetworks(self, ripNetworks:str) -> list:
        return ripNetworks.split(',')

    # Define the string representation of the class
    def __repr__(self) -> str:
        ripSumState = "Auto Summary: " + self.ripSumState + "\n" if self.ripSumState else ''
        ripOriginate = "Default Information Originate: " + self.ripOriginate + "\n" if self.ripOriginate else ''

        return "RIP Version: " + self.ripVersion + "\n" + "Auto Summary: " + ripSumState + "\n" + "Default Information Originate: " + ripOriginate + "\n" + "Networks: " + ', '.join(self.ripNetworks) + "\n"
    
    # Convert the stored RIP routing configurations to a list of configuration commands
    def toConfig(self) -> list:
        ripSumState = "Auto Summary: " + self.ripSumState + "\n" if self.ripSumState else ''
        ripOriginate = "Default Information Originate: " + self.ripOriginate + "\n" if self.ripOriginate else ''
        config = []
        config.append("router rip\n")
        config.append(f" version {self.ripVersion}\n")
        if self.ripSumState:
            config.append(f" {ripSumState}")
        if self.ripOriginate:
            config.append(f" {ripOriginate}")
        for network in self.ripNetworks:
            config.append(f" network {network}\n")
        config.append("!\n")
        return config

#endregion
#region DHCP

# Define a class to manage DHCP configurations
class DHCP:
    # Initialize the class with various parameters
    def __init__(self, dhcpNetworkIP:str = None,dhcpNetworkSM:str = None, dhcpGateway:str = None, dhcpDNS:str = None, dhcpExcludedAreas:str = None, dhcpPoolName:str = None) -> None:
        # Check if the dhcpNetworkIP is a string and store it
        if type(dhcpNetworkIP) == str:
            self.dhcpNetworkIP = dhcpNetworkIP
        else:
            raise TypeError()
        
        # Check if the dhcpNetworkSM is a string and store it
        if type(dhcpNetworkSM) == str:
            self.dhcpNetworkSM = dhcpNetworkSM
        else:
            raise TypeError()

        # Check if the dhcpGateway is a string and store it
        if type(dhcpGateway) == str:
            self.dhcpGateway = dhcpGateway
        else:
            raise TypeError()
        
        # Check if the dhcpDNS is a string and store it
        if type(dhcpDNS) == str:
            self.dhcpDNS = dhcpDNS
        else:
            raise TypeError()
        
        # Check if the dhcpExcludedAreas is a string and store it
        if type(dhcpExcludedAreas) == str:
            self.areas = []
            self.getAreas(dhcpExcludedAreas)
        else:
            raise TypeError()
        
        # Check if the dhcpPoolName is a string and store it
        if type(dhcpPoolName) == str:
            self.dhcpPoolName = dhcpPoolName
        else:
            raise TypeError()
        
    # Split the dhcpExcludedAreas string into individual areas and store them in a list
    def getAreas(self, dhcpExcludeAreas:str) -> list:
        if dhcpExcludeAreas:
            areas = dhcpExcludeAreas.split(';')
            for area in areas:
                if(len(area) < 1):
                    continue
                AreaFromIP, AreaToIP = area.split(',')
                self.areas.append({'AreaFromIP': AreaFromIP, 'AreaToIP': AreaToIP})
        return self.areas
    
    # Define the string representation of the class
    def __repr__(self) -> str:
        excluded_areas = ', '.join([f"{area['AreaFromIP']} - {area['AreaToIP']}" for area in self.areas])
        return (
            f"Network IP: {self.dhcpNetworkIP}\n"
            f"Network Subnet Mask: {self.dhcpNetworkSM}\n"
            f"Gateway: {self.dhcpGateway}\n"
            f"DNS: {self.dhcpDNS}\n"
            f"Excluded Areas: {excluded_areas}\n"
            f"Pool Name: {self.dhcpPoolName}\n"
        )
    # Convert the stored DHCP configurations to a list of configuration commands
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

# Define a class to manage Network Address Translation (NAT) configurations
class NAT:
    # Initialize the class with various parameters
    def __init__(self, interfaceName:str = None, accessListName:str = None) -> None:
        # Check if the interfaceName is a string and store it
        if type(interfaceName) == str:
            self.interface = interfaceName
        else:
            raise TypeError()
        
        # Check if the accessListName is a string and store it
        if type(accessListName) == str:
            self.accessList = accessListName
        else:
            raise TypeError()
    
    # Define the string representation of the class
    def __repr__(self) -> str:
        return "Interface: " + self.interface + "\n" + "Access List: " + self.accessList + "\n"
    
    # Convert the stored NAT configurations to a list of configuration commands
    def toConfig(self) -> list:
        config = []
        config.append(f"ip nat inside source list {self.accessList} interface {self.interface} overload\n" + "!\n")
        return config
#endregion
#region ACL

# Define a class to manage Standard Access Control List (ACL) configurations
class ACLStandard:
    # Initialize the class with various parameters
    def __init__(self, accessList:str = None, accessListName:str = None) -> None:
        # Check if the accessList is a string and store it
        if type(accessList) == str:
            self.ACLs = []
            self.getACLs(accessList)
        else:
            raise TypeError()  
        if type(accessListName) == str:
            self.accessList = accessListName
        else:
            raise TypeError()

    # Split the accessList string into individual ACLs and store them in a list
    # The accessList string format is "ACLID,deny|permit,IP,SM;ACLID,deny|permit,IP,SM;ACLID,IP,SM"
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

    # Define the string representation of the class
    def __repr__(self) -> str:
        return "AccessListName: " + self.accessListName + "\n" + json.dumps(self.ACL, indent=4)
    
    # Convert the stored ACL configurations to a list of configuration commands
    def toConfig(self) -> list:
        config = []
        config.append(f"ip access-list standard {self.accessListName}\n")
        for acl in self.ACLs:
            if len(acl) == 3:
                config.append(f"access-list {acl['id']} {acl['permitDeny']} {acl['ip']}\n")
            elif len(acl) == 4:
                config.append(f"access-list {acl['id']} {acl['permitDeny']} {acl['ip']} {acl['sm']}\n")
        config.append("!\n")
        return config
    
#endregion
#region OSPF
 
# Define a class to manage OSPF (Open Shortest Path First) configurations
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
        
        self.ospfNetworks = []
        if type(ospfNetworks) == str:
            self.getNetworks(ospfNetworks)
        else:
            raise TypeError()

    def getNetworks(self, ospfNetworks:str) -> list:
        if ospfNetworks:
            networks = ospfNetworks.split(';')
            for network in networks:
                if network:
                    networkID, networkWM, area = network.split(',')
                    self.ospfNetworks.append({'networkID': networkID, 'networkWM': networkWM, 'area': area})
        return self.ospfNetworks
    
    # Define the string representation of the class
    def __repr__(self) -> str:
        networks = ', '.join([f"{network['networkID']}, {network['networkWM']}, {network['area']}" for network in self.ospfNetworks])
        return "OSPF Process: " + self.ospfProcess + "\n" + "Router ID: " + self.ospfRouterID + "\n" + "Networks: " + networks + "\n"

    # Convert the stored OSPF configurations to a list of configuration commands
    def toConfig(self) -> list:
        config = []
        config.append("router ospf " + self.ospfProcess + "\n")
        config.append(f" router-id {self.ospfRouterID}\n")
        for network in self.ospfNetworks:
            config.append(f" network {network['networkID']} {network['networkWM']} area {network['area']}\n")
        config.append("!\n")
        return config

#endregion
#region ACL Extended
class ACLExtended:
    def __init__(self, aclListName:str = None, aclList:list = None) -> None:
        if aclList is None:
            self.aclList = []
        elif type(aclList) == list:
            self.aclList = aclList
        else:
            raise TypeError()
        if type(aclListName) == str:
            self.aclListName = aclListName
        else:
            raise TypeError()
    
    def getACLs(self, aclList:str) -> list:
        if aclList:
            ACLs = aclList.split(";")
            for ACL in ACLs:
                if ACL:
                    id, permitDeny, protocol, sourceIP, sourceWM, destIP, destWM, port = ACL.split(",")
                    self.aclList.append({'id': id, 'permitDeny': permitDeny, 'protocol': protocol, 'sourceIP': sourceIP, 'sourceWM': sourceWM, 'destIP': destIP, 'destWM': destWM, 'port': port})
        return self.aclList
    
    def __repr__(self) -> str:
        return "AccessListName: " + self.aclListName + "\n" + json.dumps(self.aclList, indent=4)

    def toConfig(self) -> list:
        #! FORMAT ERROR
        #! FORMAT ERROR
        #! FORMAT ERROR
        #! FORMAT ERROR
        #^ip access-list extended test
        #^ permit tcp 1.1.1.0 0.0.0.255 2.2.2.0 0.0.0.255 eq www
        #^ permit tcp any any eq www
        #^!
        #^ip access-list extended test2
        #^ permit tcp 1.1.1.0 0.0.0.255 2.2.2.0 0.0.0.255 eq www
        #^ permit tcp any any eq www

        #line 437: access-list and id is not required
        #maybe think about adding a check if any parameter is any


        config = []
        config.append(f"ip access-list extended {self.aclListName}\n")
        for acl in self.aclList:
            config.append(f"access-list {acl['id']} {acl['permitDeny']} {acl['protocol']} {acl['sourceIP']} {acl['sourceWM']} {acl['destIP']} {acl['destWM']} {acl['port']}\n")
        config.append("!\n")
        return config
#endregion

