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
#region Interface

# Define a class to store interface information
class Interface:
    # Initialize the class with various parameters
    def __init__(self, vlanInt:str = None, ip:str = None, sm:str = None, description:str = "Default", shutdown:bool = None, vlans:str = None, createChannelGroups:str = None, assignChannelGroups:str = None) -> None:
        # Check if the interface is a string and store it
        if type(vlanInt) == str:
            self.vlanInt = vlanInt
        else:
            raise TypeError()
        
        self.vlans = []
        if type(vlans) == str:
            self.getVLANs(vlans)
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
        
        self.channelGroups = []
        if type(assignChannelGroups) == str:
            self.getAssignChannelGroups(assignChannelGroups)

       
    #^ vlanMode,vlanNative,vlanAllowed:vlanAllowed:vlanAllowed
    def getVLANs(self, vlans:str) -> list:
        if vlans: 
            mode, nativeVLAN, allowedVLANs = vlans.split(',')
            # Split allowedVLANs by ':'
            self.vlanAllowed = allowedVLANs.split(':')
            self.vlanNative = nativeVLAN
            self.vlanMode = mode
            self.vlans.append(1)


    #^ channelMode,channeldID
    def getAssignChannelGroups(self, assignChannelGroups:str) -> list:
        if assignChannelGroups:
            mode, channelID = assignChannelGroups.split(',')
            self.channelMode = mode
            self.channelID = channelID
            self.channelGroups.append(1)

    # Define the string representation of the class
    def __repr__(self) -> str:
        return "Interface: " + self.vlanInt + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + str(self.shutdown) + "\n + VLANs: " + self.vlans + "\n"
        
    # Convert the interface information to a configuration list
    def toConfig(self) -> list:
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"
        config = []
        #! NOT WORKING YET - NEED TO IMPLEMENT
            #^ only working for itself
        if len (self.vlans) == 0 and len(self.channelGroups) == 0:
            config.append(f'interface vlan{self.vlanInt}\n')
            config.append(f' ip address {self.ip} {self.sm}\n')
            config.append(f' description {self.description}\n')
            config.append(shutdown)
            config.append('!\n')
            return config
        
        elif len (self.vlans) > 0 and len(self.channelGroups) == 0:
            config.append(f"interface {self.vlanInt}\n")
            config.append(f" switchport mode {self.vlanMode}\n")
            config.append(f" switchport trunk native vlan {self.vlanNative}\n")
            config.append(f" switchport trunk allowed vlan {self.vlanAllowed}\n")
            config.append(f" description {self.description}\n")
            config.append(shutdown)
            config.append('!\n')

        elif len (self.vlans) == 0 and len(self.channelGroups) > 0:
            config.append(f'interface {self.vlanInt}\n')
            config.append(f' channel-group {self.channelID} mode {self.channelMode}\n')
            config.append(f' description {self.description}\n')
            config.append(shutdown)

        elif len (self.vlans) > 0 and len(self.channelGroups) > 0:
            config.append(f"interface {self.vlanInt}\n")
            config.append(f" switchport mode {self.vlanMode}\n")
            config.append(f" switchport trunk native vlan {self.vlanNative}\n")
            config.append(f" switchport trunk allowed vlan {self.vlanAllowed}\n")
            config.append(f" channel-group {self.channelID} mode {self.channelMode}\n")
            config.append(f" description {self.description}\n")
            config.append(shutdown)
            config.append('!\n')
        return config
        
#region VLAN

class CreateVLANs:
    def __init__(self, vlans:str = None) -> None:
        if type(vlans) == str:
            self.vlans = vlans
        else:
            raise TypeError()

    def getVLANs(self, vlans:str) -> list:
        if vlans:
            vlans = vlans.split(';')
            for vlan in vlans:
                if vlan:
                    vlanID, vlanName = vlan.split(',')
                    self.vlans.append({"vlanID": vlanID, "vlanName": vlanName})
        return self.vlans
    
    def __repr__(self) -> str:
        return "VLANs: " + self.vlans + "\n"

    def toConfig(self) -> list:
        vlanConfig = []
        #! Vlan configs is in vlan database, views.py not ready yet.
        # for vlan in self.vlans:
        #     vlanConfig.append(f'vlan {vlan["vlanID"]}\n')
        #     vlanConfig.append(f' name {vlan["vlanName"]}\n')
        #     vlanConfig.append('!\n')
        # return vlanConfig
#endregion




