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
        
        if type(vlans) == str:
            self.vlans = []
            self.vlans = self.getVLANs(vlans)
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
        if type(createChannelGroups) == str:
            self.portChannels = []
            self.getCreateChannelGroups(createChannelGroups)
        else:
            raise TypeError()
        
        if type(assignChannelGroups) == str:
            self.channelGroups = []
            self.getAssignChannelGroups(assignChannelGroups)
        else:
            raise TypeError()
        
    #^ Interface,trunk,native_vlan,allowed_vlan:allowed_vlan;
    def getVLANs(self, vlans:str) -> list:
        if vlans:
            vlans = vlans.split(';')
            for vlan in vlans:
                if vlan:
                    interfaceID, mode, nativeVLAN, allowedVLANs = vlan.split(',')
                    # Split allowedVLANs by ':'
                    allowedVLANs = allowedVLANs.split(':')
                    self.vlans.append({"interfaceID" : interfaceID, "mode" : mode, "nativeVLAN" : nativeVLAN, "allowedVLANs" : allowedVLANs})
        return self.vlans
    
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
        return "Interface: " + self.vlanInt + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + str(self.shutdown) + "\n + VLANs: " + self.vlans + "\n"
        
    # Convert the interface information to a configuration list
    def toConfig(self) -> list:
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"
        config = []
        if len(self.vlans) > 0:
            config.append(f"interface {self.interface}\n")
            config.append(f" ip address {self.ip} {self.sm}\n" if self.ip.lower() != "dhcp" else ' ip address dhcp\n')
            config.append(f" description {self.description}\n")
            config.append(f" {shutdown}")
            config.append("!\n")
        else:
            #! NOT WORKING YET - NEED TO IMPLEMENT
            #^ only working for itself7
            for vlan in self.vlans:
                print(vlan)
                config.append(f"interface {vlan['interfaceID']}\n")
                config.append(f" switchport mode {vlan['mode']}\n")
                config.append(f" switchport trunk native vlan {vlan['nativeVLAN']}\n")
                config.append(f" switchport trunk allowed vlan {vlan['allowedVLANs']}\n")
                config.append(f" switchport {vlan['mode']} encapsulation dot1q\n")
                config.append(f" {shutdown}")
                config.append(f" description {self.description}\n")
                config.append("!\n")
            return config

#~ Testing vlan Config
# vlanINT = Interface(vlanInt='10', ip='192.168.30.100', sm='255.255.255.0', description='TestTest', shutdown=True, vlans='5,trunk,1,10:20:30;15,access,1,10:20:30;')
# config = vlanINT.toConfig()
# for line in config:
#     print(line)

#endregion
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




