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
        return [f"hostname {self.hostname}\n", "!\n", f"banner motd ^C{self.motd}^C\n", "!\n"]
#endregion
#region Interfaces

# Define a class to store interface information
class Interface:
    # Initialize the class with various parameters
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, ipNatInside:bool = None, ipNatOutside:bool = None, description:str = "Default", shutdown:bool = None , createChannelGroups:str = None, assignChannelGroups:str = None ) -> None:
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
        
        if type(createChannelGroups) == str:
            self.portChannels = []
            self.getCreateChannelGroups(createChannelGroups)
        
        if type(assignChannelGroups) == str:
            self.channelGroups = []
            self.getAssignChannelGroups(assignChannelGroups)

        
    def getCreateChannelGroups(self, createChannelGroups:str) -> list:
        if createChannelGroups:
            portChannels = createChannelGroups.split(';')
            for portChannel in portChannels:
                if portChannel:
                    channelID, channelIP, channelSM = portChannel.split(',')
                    self.portChannels.append({'channelID': channelID, 'channelIP': channelIP, 'channelSM': channelSM})
        return self.portChannels


    def getAssignChannelGroups(self, assignChannelGroups:str) -> list:
        if assignChannelGroups:
            channelGroups = assignChannelGroups.split(';')
            for channelGroup in channelGroups:
              if channelGroup:
                channelInterface, channelID, channelMode = channelGroup.split(',')
                self.channelGroups.append({'channelInterface': channelInterface, 'channelID': channelID, 'channelMode': channelMode})
        return self.channelGroups 
        

    # Define the string representation of the class
    def __repr__(self) -> str:
        natInside = "ip nat inside\n" if self.ipNatInside else ''
        natOutside = "ip nat outside\n" if self.ipNatOutside else ''
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"

        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + shutdown + "\n" + natInside + natOutside 

    # Convert the interface information to a configuration list
    def toConfig(self) -> list:
        config = []
        natInside = "ip nat inside\n" if self.ipNatInside else ''
        natOutside = "ip nat outside\n" if self.ipNatOutside else ''
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"
        if len (self.channelGroups) < 0:
            config.append(f"interface {self.interface}\n")
            config.append(f" ip address {self.ip} {self.sm}\n" if self.ip.lower() != "dhcp" else ' ip address dhcp\n')
            config.append(f" description {self.description}\n")
            config.append(f" {shutdown}")
            config.append(f" {natInside}")
            config.append(f" {natOutside}")
            config.append("!\n")
        else:
            for channelGroup in self.channelGroups:
                config.append(f"interface {channelGroup['channelInterface']}\n")
                config.append(f" ip address {self.ip} {self.sm}\n" if self.ip.lower() != "dhcp" else ' ip address dhcp\n')
                config.append(f" description {self.description}\n")
                config.append(f" {shutdown}")
                config.append(f" {natInside}")
                config.append(f" {natOutside}")
                config.append(f" channel-group {channelGroup['channelID']} mode {channelGroup['channelMode']}\n")
                config.append("!\n")
        if len(self.portChannels) > 0:
            for portChannel in self.portChannels:
                config.append(f"interface Port-channel {portChannel['channelID']}\n")
                config.append(f" ip address {portChannel['channelIP']} {portChannel['channelSM']}\n")
                config.append("!\n")
        return config 
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
    # Define the string representation of the class
    def __repr__(self) -> str:
        ripSumState = "no auto-summary\n " if self.ripSumState else 'auto-summary\n'
        ripOriginate = "default-information originate " if self.ripOriginate else ''

        return "RIP Version: " + self.ripVersion + "\n" + ripSumState + ripOriginate + "Networks: " + ', '.join(self.ripNetworks) + "\n"

    # Convert the stored RIP routing configurations to a list of configuration commands
    def toConfig(self) -> list:
        ripSumState = " no auto-summary\n" if self.ripSumState else " auto-summary\n"
        ripOriginate = " default-information originate\n" if self.ripOriginate else ''
        config = []
        config.append("router rip\n")
        config.append(f" version {self.ripVersion}\n")
        config.append(ripSumState)
        if self.ripOriginate:
            config.append(ripOriginate)
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
    def __init__(self, accessList:str = None) -> None:
        # Check if the accessList is a string and store it
        if type(accessList) == str:
            self.ACLs = []
            self.getACLs(accessList)
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
        return  json.dumps(self.ACL, indent=4)
    
    # Convert the stored ACL configurations to a list of configuration commands
    def toConfig(self) -> list:
        config = []
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
    def __init__(self, ospfProcess:str = None, ospfRouterID:str = None, ospfOriginate:bool = None, ospfAutoSummary:bool = None, ospfNetworks:str = None) -> None:
        if type(ospfProcess) == str:
            self.ospfProcess = ospfProcess
        else:
            raise TypeError()
        
        if type(ospfRouterID) == str:
            self.ospfRouterID = ospfRouterID
        else:
            raise TypeError()
        
        if type(ospfNetworks) == str:
            self.ospfNetworks = []
            self.getNetworks(ospfNetworks)
        else:
            raise TypeError()
        
        if type(ospfOriginate) == bool:
            self.ospfOriginate = ospfOriginate
        else:
            raise TypeError()
        
        if type(ospfOriginate) == bool:
            self.ospfAutoSummary = ospfAutoSummary
        else:
            raise TypeError()
        
    # If ospfNetworks is not empty, it splits the string into individual networks.
        # For each network, it splits the string into individual fields and appends them as a dictionary to the ospfNetworks list.
        # It returns the ospfNetworks list.
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
        ospfAutoSummary = " no auto-summary\n" if self.ospfAutoSummary else ' auto-summary\n'
        ospfOriginate = " default-information originate\n" if self.ospfOriginate else ''
        networks = ', '.join([f"{network['networkID']}, {network['networkWM']}, {network['area']}" for network in self.ospfNetworks])
        return "OSPF Process: " + self.ospfProcess + "\n" + "Router ID: " + self.ospfRouterID + "\n" + "Networks: " + networks + "\n" + "Default Information Originate: " + ospfOriginate + "\n" + "Auto Summary: " + ospfAutoSummary + "\n"

    # It initializes an empty list and appends the OSPF process and router ID to it.
    # For each network in the ospfNetworks list, it appends a string of the network fields to the list.
    # Convert the stored OSPF configurations to a list of configuration commands
    def toConfig(self) -> list:
        ospfAutoSummary = " no auto-summary\n" if self.ospfAutoSummary else ''
        ospfOriginate = " default-information originate\n" if self.ospfOriginate else ''
        config = []
        config.append("router ospf " + self.ospfProcess + "\n")
        config.append(f" router-id {self.ospfRouterID}\n")
        for network in self.ospfNetworks:
            config.append(f" network {network['networkID']} {network['networkWM']} area {network['area']}\n")
        config.append(ospfOriginate)
        config.append(ospfAutoSummary)
        config.append("!\n")
        return config

#endregion
#region ACL Extended
class ACLExtended:
    def __init__(self, aclList:str = None, aclRuleName:str = None) -> None:
        if type(aclList) == str:
            # self.aclList = aclList
            self.aclList = []
            self.getACLs(aclList)
        else:
            raise TypeError()
        
        if type(aclRuleName) == str:
            self.aclRuleName = aclRuleName
        else:
            raise TypeError()
        
    # If aclList is not empty, it splits the string into individual ACLs.
    # For each ACL, it splits the string into individual fields and appends them as a dictionary to the aclList list.
    # It returns the aclList list.
    def getACLs(self, aclList:str) -> list:
        if aclList:
            ACLs = aclList.split(";")
            for ACL in ACLs:
                if ACL:
                    permitDeny, protocol, sourceIP, sourceWM, destIP, destWM, port = ACL.split(",")
                    self.aclList.append({'permitDeny': permitDeny, 'protocol': protocol, 'sourceIP': sourceIP, 'sourceWM': sourceWM, 'destIP': destIP, 'destWM': destWM, 'port': port})
        return self.aclList
    
    def __repr__(self) -> str:
        return self.aclRuleName + json.dumps(self.aclList, indent=4)


     # It initializes an empty list and appends the ACL rule name to it.
        # For each ACL in the aclList list, it appends a string of the ACL fields to the list.
        # It appends a "!" to the list and returns it.
    def toConfig(self) -> list:
        config = []
        config.append(f"ip access-list extended {self.aclRuleName}\n")
        for acl in self.aclList:
            config.append(f" permit {acl['protocol']} {acl['sourceIP']} {acl['sourceWM']} {acl['destIP']} {acl['destWM']} eq {acl['port']}\n")
        config.append("!\n")
        return config
#endregion
