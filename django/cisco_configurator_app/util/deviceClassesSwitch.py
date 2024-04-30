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
    def __init__(self, interface:str = None, ip:str = None, sm:str = None, description:str = "Default", shutdown:bool = None ) -> None:
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

    # Define the string representation of the class
    def __repr__(self) -> str:
        shutdown = "shutdown\n" if self.shutdown else "no shutdown\n"

        return "Interface: " + self.interface + "\n" + "IP: " + self.ip + "\n" + "Subnet Mask: " + self.sm + "\n" + "Description: " + self.description + "\n" + "Shutdown: " + shutdown + "\n" 

    # Convert the interface information to a configuration list
    def toConfig(self) -> list:
        ipConfig = f' ip address {self.ip} {self.sm}\n' if self.ip.lower() != "dhcp" else ' ip address dhcp\n'

            
        return ["interface " + self.interface + "\n", ipConfig, f' description {self.description}\n', f' {self.shutdown}', f' {natInside}', f'{natOutside}' + "!\n"]

#endregion
