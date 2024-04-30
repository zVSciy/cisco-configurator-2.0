from .configEditor import configEditor
from .deviceClasses import Interface, StaticRoute, RipRouting, DHCP, ACLStandard, NAT, DeviceInfo 

#! This file colored comments to highlight the different sections of the code
#! THis extention was used: ParthR2031.colorful-comments
#! The colors are as follows:
#^ For examples from the exampleConfig
#! for important things 





class ConfigManager:
    def __init__(self, configFilePath:str) -> None:
        #The filepath of the input file
        self.filePath = configFilePath
        #The configEditor object that will be used to read and write the config file
        self.configEditor = configEditor(configFilePath)


    #region BasicConfig

    # Returns a DeviceInfo object with the hostname and motd configuration in the config file
    def getDeviceInfo(self) -> str:
        hostNameLine = self.configEditor.findContentIndexes("hostname ", "!")
        motdLine = self.configEditor.findContentIndexes("banner motd ", "!")
        hostName = self.configEditor.getContentOnIndex(hostNameLine[0]).split(" ")[1]
        #^hostname R1
        motd = self.configEditor.getContentOnIndex(motdLine[0])
        #^banner motd ^Chello^C
        return DeviceInfo(hostName, motd)
    
    def writeDeviceInfo(self, deviceInfo: DeviceInfo) -> None:
        hostNameLine = self.configEditor.findContentIndexes("hostname ", "!")
        if(len(hostNameLine) > 0):
            self.configEditor.removeContentBetweenIndexes(hostNameLine[0], hostNameLine[-1])
        motdLine = self.configEditor.findContentIndexes("banner motd ", "!")
        if(len(motdLine) > 0):
            self.configEditor.removeContentBetweenIndexes(motdLine[0], motdLine[-1])
        self.configEditor.appendContentToFile(deviceInfo.toConfig())
        self.configEditor.writeConfig()
    #endregion


    #region Interfaces

    # Returns an Interface object based on the interface name.
    # It searches for the interface name in the config file and returns the object
    #! Note the interfaceName should be the name of the interface without the "interface" keyword -> "FastEthernet0/1" instead of "interface FastEthernet0/1"
    def getInterface(self, interfaceName: str) -> Interface:
        InterfaceLines = self.configEditor.findContentIndexes("interface " + interfaceName, "!") #Finds the indexes of the interface in the config list
        interfaceText = self.configEditor.getContentBetweenIndexes(InterfaceLines[0], InterfaceLines[-1]) #Gets the content of the interface
        intName, ip, sm, desc, natInside, natOutside, shut = None, None, None, "Default", None, None, True
        #Iterates over the lines of the interface, splits the line and assigns the values to the variables
        for intLine in interfaceText: #Iterates over the lines of the interface
            if intLine.startswith("interface "):
                #^ interface FastEthernet0/0
                intName = intLine.split(" ")[1]
            elif intLine.startswith("ip address"):
                #^ ip address 192.168.2.1 255.255.255.0
                ip = intLine.split(" ")[2]
                if len(intLine.split(" ")) > 3:
                    sm = intLine.split(" ")[3]
                else :
                    sm = ''
            elif intLine.startswith("ip nat"):
                #^ ip nat inside
                #^ ip nat outside
                nat = intLine.split(" ")[2]
                natInside = True if nat == "inside" else False
                natOutside = True if nat == "outside" else False
            elif intLine.startswith("description"):
                #^ description value
                desc = intLine.split(" ")[1]
            elif intLine.startswith("shutdown") or intLine.startswith("no shutdown"):
                #^ no shutdown
                #^ shutdown
                shut = False if intLine == "shutdown" else True
            if natInside == None: natInside = False
            if natOutside == None: natOutside = False
        return Interface(intName, ip, sm, natInside, natOutside, desc, shut)
    
    # returns a list of all Interfaces in the config file
    def getAllInterfaces(self) -> list[Interface]:
        InterfacesLines = self.configEditor.findMultipleContentIndexes("interface ")
        returnInterfaceObjects = []
        print(InterfacesLines)
        for interfaceIndexes in InterfacesLines:
            interfaceText = self.configEditor.getContentOnIndex(interfaceIndexes[0])
            intName = interfaceText.split(" ")[1]
            #^ interface FastEthernet0/0
            returnInterfaceObjects.append(self.getInterface(intName))
        return returnInterfaceObjects
    
    # Writes the interface object to the config file
    # If a interface with the same name is detected, it will replace it, if no interface is found, it will add a new interface to the end of the file
    def writeInterface(self, interface: Interface) -> None:
        interfaceLines = self.configEditor.findContentIndexes("interface " + interface.interface, "!")
        if(len(interfaceLines) > 0 and interfaceLines != None):
            self.configEditor.removeContentBetweenIndexes(interfaceLines[0], interfaceLines[-1])
        self.configEditor.appendContentToFile(interface.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region Static Routes

    # returns a StaticRoute object with all the static routes in the config file
    def getStaticRoutes(self) -> StaticRoute:
        staticRoutesLines = self.configEditor.findContentIndexes("ip route ")
        returnStaticRoutes = ""
        for routeIndex in staticRoutesLines:
            routeText = self.configEditor.getContentOnIndex(routeIndex).split(" ")
            #^ ip route 192.168.1.0 255.255.255.0 192.168.1.6
            targetNw = routeText[2]
            targetSm = routeText[3]
            nextHop = routeText[4]
            #If the content of returnStaticRoutes is not empty, add a semicolon to separate the routes, if this doesnt happen the first route will have a semicolon in front of it
            if len(returnStaticRoutes) > 0:
                returnStaticRoutes += ";"
            returnStaticRoutes += targetNw + "," + targetSm + "," + nextHop
        return StaticRoute(returnStaticRoutes)
    
    # Writes the static routes to the config file
    # Replaces all current static routes with the ones inside the staticRoutes object
    def writeStaticRoutes(self, staticRoutes: StaticRoute) -> None:
        staticRouteLines = self.configEditor.findContentIndexes("ip route ")
        self.configEditor.removeContentBetweenIndexes(staticRouteLines[0], staticRouteLines[-1])
        self.configEditor.appendContentToFile(staticRoutes.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region RIP

    # Returns a RipRouting object with the RIP configuration in the config file
    # It searches for the "router rip" keyword and reads the configuration
    def getRIPConfig(self) -> RipRouting:
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        ripText = self.configEditor.getContentBetweenIndexes(ripLines[0], ripLines[-1])
        ripNetworks = []
        ripVersion, ripSumState, ripOriginate, ripNetworks = None, False, False, ""
        for ripLine in ripText:
            if ripLine.startswith("version"):
                #^ version 2
                ripVersion = ripLine.split(" ")[1]
            elif ripLine.startswith("no-auto summary"):
                #^ no auto summary
                ripSumState = True
            elif ripLine.startswith("default-information originate"):
                #^ default-information originate
                ripOriginate = True
            elif ripLine.startswith("network"):
                #^ network 192.168.0.1
                #If the ripNetworks string is not empty, add a semicolon to separate the networks
                if len(ripNetworks) > 0:
                    ripNetworks += ";"
                ripNetworks += ripLine.split(" ")[1]
            
        return RipRouting(ripVersion, ripSumState, ripOriginate, ripNetworks)
    
    # Writes the RIP configuration to the config file
    # Replaces the current RIP configuration with the one in the ripConfig object
    def writeRIPConfig(self, ripConfig: RipRouting) -> None:
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        self.configEditor.removeContentBetweenIndexes(ripLines[0], ripLines[-1])
        self.configEditor.appendContentToFile(ripConfig.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region DHCP

    # Returns a DHCP object with the DHCP configuration in the config file
    # Also searches for excluded addresses and adds them to the DHCP object, because they are in a seperate part of the configuration
    def getDhcpConfig(self, inputPoolName: str ) -> DHCP:
        dhcpLines = self.configEditor.findContentIndexes(f"ip dhcp pool {inputPoolName}", "!")
        dhcpText = self.configEditor.getContentBetweenIndexes(dhcpLines[0], dhcpLines[-1])
        excludedLines = self.configEditor.findContentIndexes("ip dhcp excluded-address", "!")
        excludedText = self.configEditor.getContentBetweenIndexes(excludedLines[0], excludedLines[-1])
        poolName, networkIP, networkSM, defaultRouter, dnsServer = None, None, None, None, None
        excludedNetworks = ""
        for line in dhcpText:
            if line.startswith("ip dhcp pool"):
                #^ ip dhcp pool 172
                poolName = line.split(" ")[3]
            elif line.startswith("network"):
                #^ network 172.16.11.0 255.255.255.0
                networkIP = line.split(" ")[1]
                networkSM = line.split(" ")[2]
            elif line.startswith("default-router"):
                #^ default-router 172.16.11.1
                defaultRouter = line.split(" ")[1]
            elif line.startswith("dns-server"):
                #^ dns-server 8.8.8.8
                dnsServer = line.split(" ")[1]

        for line in excludedText:
            # if the excludedNetworks string is not empty, add a semicolon to separate the networks
            if(len(excludedNetworks) > 0):
                excludedNetworks += ";"

            #^ ip dhcp excluded-address 172.16.11.0 172.16.11.10
            excludedNetworks += line.split(" ")[3] + "," + line.split(" ")[4]
        return DHCP(networkIP, networkSM, defaultRouter, dnsServer, excludedNetworks, poolName)

    # Writes the DHCP configuration to the config file
    def writeDhcpConfig(self, dhcpConfig: DHCP) -> None:
        #get the dhcp lines
        dhcpLines = self.configEditor.findContentIndexes(f"ip dhcp pool {dhcpConfig.dhcpPoolName}", "!")
        #get excluded lines
        excludedLines = self.configEditor.findContentIndexes("ip dhcp excluded-address", "!")
        #check if something was found, if it wasnt, create a new pool
        if(len(dhcpLines) > 0):
            self.configEditor.removeContentBetweenIndexes(dhcpLines[0], dhcpLines[-1])
        if(len(excludedLines) > 0):
            self.configEditor.removeContentBetweenIndexes(excludedLines[0], excludedLines[-1])
        self.configEditor.appendContentToFile(dhcpConfig.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region ACL

    # Returns an ACLStandard object with the ACL configuration in the config file

    def getACLConfig(self) -> ACLStandard:
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        aclText = self.configEditor.getContentBetweenIndexes(aclLines[0], aclLines[-1])
        ACLs = "" #^"ACLID,deny|permit,IP,SM;ACLID,deny|permit,IP,SM;ACLID,IP,SM"
        #Iterates over the lines of the ACL configuration and adds them to the ACLs string
        # ^ access-list 1 permit any
        # ^ access-list 2 permit 192.168.1.1 123.123.123.123
        for line in aclText:
            if not line.startswith("access-list"):
                continue
            if len(ACLs) > 0:
                ACLs += ";"
            aclID = line.split(" ")[1]
            aclType = line.split(" ")[2]
            aclIP = line.split(" ")[3]
            if aclIP == "any":
                ACLs += aclID + "," + aclType + "," + aclIP
            else:
                aclWM = line.split(" ")[4]
                ACLs += aclID + "," + aclType + "," + aclIP + "," + aclWM
        return ACLStandard(ACLs)
    
    # Writes the ACL configuration to the config file
    def writeACLConfig(self, aclConfig: ACLStandard) -> None:
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        if(len(aclLines) > 0):
            self.configEditor.removeContentBetweenIndexes(aclLines[0], aclLines[-1])
        self.configEditor.appendContentToFile(aclConfig.toConfig())
        self.configEditor.writeConfig()


    #region NAT

    # Returns a NAT object with the NAT configuration in the config file
    def getNATConfig(self) -> NAT:
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        natText = self.configEditor.getContentBetweenIndexes(natLines[0], natLines[-1])
        #^ip nat inside source list 1 interface Ethernet0/1 overload
        for line in natText:
            if line.startswith("ip nat inside source"):
                aclName = line.split(" ")[5]
                interfaceName = line.split(" ")[7]
            return NAT(interfaceName, aclName)

    # Writes the NAT configuration to the config file
    def writeNATConfig(self, natConfig: NAT) -> None:
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        if(len(natLines) > 0):
            self.configEditor.removeContentBetweenIndexes(natLines[0], natLines[-1])
        self.configEditor.appendContentToFile(natConfig.toConfig())
        self.configEditor.writeConfig()

    #endregion




# region Example Usage

# filePath = "./exampleConfig"
# cM = ConfigManager(filePath)

# print(cM.getAllInterfaces())
# for i in cM.getAllInterfaces():
#     print(i.toConfig())
#     cM.writeInterface(i)

# int =  cM.getInterface("Fast")
# cM.writeInterface(int)

# print(cM.getStaticRoutes().toConfig())

# interface = cM.getInterface("FastEthernet0/1")
# interface.ip = '10.10.23.11'
# cM.writeInterface(interface)

# staticRoutes = cM.getStaticRoutes()
# cM.writeStaticRoutes(staticRoutes)

# print(cM.getRIPConfig().toConfig())

# # print(cM.getDhcpConfig("172"))
# print(cM.getDhcpConfig("172").toConfig())
# dhcpConfig = cM.getDhcpConfig("172")
# cM.writeDhcpConfig(dhcpConfig)

# ripConfig = cM.getRIPConfig()
# ripConfig.ripVersion = "1"
# cM.writeRIPConfig(ripConfig)

# print(cM.getACLConfig().toConfig())
# cM.writeACLConfig(cM.getACLConfig())

# natConfig = cM.getNATConfig()
# natConfig.accessList = "5"
# cM.writeNATConfig(natConfig)

#endregion

