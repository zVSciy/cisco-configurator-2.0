from .configEditor import configEditor
from .deviceClasses import Interface, StaticRoute, RipRouting, DHCP, ACLStandard, NAT, DeviceInfo, ACLExtended, OSPF

#! This file colored comments to highlight the different sections of the code
#! THis extention was used: ParthR2031.colorful-comments
#! The colors are as follows:
#^ For examples from the exampleConfig
#! for important things 





class ConfigManager:
    def __init__(self, configFilePath:str, configOutputPath: str = None) -> None:
        #The filepath of the input file
        self.filePath = configFilePath
        self.outputPath = configOutputPath if configOutputPath != None else configFilePath
        #The configEditor object that will be used to read and write the config file
        self.configEditor = configEditor(self.filePath,self.outputPath)

    #region BasicConfig

    def getDeviceInfo(self) -> DeviceInfo:
        """Returns a DeviceInfo object with the hostname and motd configuration in the config file"""

        hostNameLine = self.configEditor.findContentIndexes("hostname ", "!")
        motdLine = self.configEditor.findContentIndexes("banner motd ", "!")
        if len(motdLine) > 0:
            motd = self.configEditor.getContentOnIndex(motdLine[0])
            #^banner motd ^Chello^C
        else:
            motd = "^C^C"

        if len(hostNameLine) > 0:
            hostName = self.configEditor.getContentOnIndex(hostNameLine[0]).split(" ")[1]
            #^hostname R1
        else :
            hostName = "DefaultHostname"
        return DeviceInfo(hostName, motd)
    
    def writeDeviceInfo(self, deviceInfo: DeviceInfo) -> None:
        """Writes the hostname and motd configuration from DeviceInfo to the config file"""
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

    #! Note the interfaceName should be the name of the interface without the "interface" keyword -> "FastEthernet0/1" instead of "interface FastEthernet0/1"
    def getInterface(self, interfaceName: str) -> Interface:
        """
        Returns an Interface object based on the interface name.
        It searches for the interface name in the config file and returns the object
        """
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

            if ip == None:
                ip = ""
            if sm == None:
                sm = ""

        return Interface(intName, ip, sm, natInside, natOutside, desc, shut)
    
    # returns a list of all Interfaces in the config file
    def getAllInterfaces(self) -> list[Interface]:
        """
        Returns a list of all Interface objects in the config file
        It searches for the "interface" keyword and reads the configuration of each interface
        """
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
        """
        Writes the interface object to the config file
        If a interface with the same name is detected, it will replace it, if no interface is found, it will add a new interface to the end of the file
        """
        interfaceLines = self.configEditor.findContentIndexes("interface " + interface.interface, "!")
        if(len(interfaceLines) > 0 and interfaceLines != None):
            self.configEditor.removeContentBetweenIndexes(interfaceLines[0], interfaceLines[-1])
        self.configEditor.appendContentToFile(interface.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region Static Routes

    # returns a StaticRoute object with all the static routes in the config file
    def getStaticRoutes(self) -> StaticRoute:
        """
        returns a StaticRoute object with all the static routes in the config file
        It searches for the "ip route" keyword and reads the configuration of each static route
        """
        staticRoutesLines = self.configEditor.findContentIndexes("ip route ")
        if len(staticRoutesLines) == 0:
            return StaticRoute("")
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
        """
        Writes the static routes to the config file
        Replaces all current static routes with the ones inside the staticRoutes object
        """
        staticRouteLines = self.configEditor.findContentIndexes("ip route ")
        if len(staticRouteLines) > 0: 
            self.configEditor.removeContentBetweenIndexes(staticRouteLines[0], staticRouteLines[-1])
        self.configEditor.appendContentToFile(staticRoutes.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region RIP

    # Returns a RipRouting object with the RIP configuration in the config file
    # It searches for the "router rip" keyword and reads the configuration
    def getRIPConfig(self) -> RipRouting:
        """"
        Returns a RipRouting object with the RIP configuration in the config file
        It searches for the "router rip" keyword and reads the configuration
        """
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        if len(ripLines) == 0:
            return RipRouting("", False, False, "") #If no RIP configuration is found, return an empty RipRouting object
        ripText = self.configEditor.getContentBetweenIndexes(ripLines[0], ripLines[-1])
        ripNetworks = []
        ripVersion, ripSumState, ripOriginate, ripNetworks = None, False, False, ""
        for ripLine in ripText:
            if ripLine.startswith("version"):
                #^ version 2
                ripVersion = ripLine.split(" ")[1]
            elif ripLine.startswith("no auto-summary"):
                #^ no auto summary
                ripSumState = True
            elif ripLine.startswith("default-information originate"):
                #^ default-information originate
                ripOriginate = True
            elif ripLine.startswith("network"):
                #^ network 192.168.0.1
                #If the ripNetworks string is not empty, add a semicolon to separate the networks
                if len(ripNetworks) > 0:
                    ripNetworks += ","
                ripNetworks += ripLine.split(" ")[1]
            
        return RipRouting(ripVersion, ripSumState, ripOriginate, ripNetworks)
    
    # Writes the RIP configuration to the config file
    # Replaces the current RIP configuration with the one in the ripConfig object
    def writeRIPConfig(self, ripConfig: RipRouting) -> None:
        """
        Writes the RIP configuration to the config file
        Replaces the current RIP configuration with the one in the ripConfig object
        """
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        if(len(ripLines) > 0):
            self.configEditor.removeContentBetweenIndexes(ripLines[0], ripLines[-1])

        self.configEditor.appendContentToFile(ripConfig.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region DHCP

    # Returns a DHCP object with the DHCP configuration in the config file
    # Also searches for excluded addresses and adds them to the DHCP object, because they are in a seperate part of the configuration
    def getDhcpConfig(self, inputPoolName: str ) -> DHCP:
        """
        Returns a DHCP object with the DHCP configuration in the config file
        Also searches for excluded addresses and adds them to the DHCP object, because they are in a seperate part of the configuration
        """
        dhcpLines = self.configEditor.findContentIndexes(f"ip dhcp pool {inputPoolName}", "!")
        if len(dhcpLines) == 0:
            return DHCP("", "", "", "", "", "")
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
        """
        Writes the DHCP configuration to the config file
        """
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
        """
        Returns an ACLStandard object with the ACL configuration in the config file
        """
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        if len(aclLines) == 0:
            return ACLStandard("")
        aclText = self.configEditor.getContentBetweenIndexes(aclLines[0], aclLines[-1])
        ACLs = "" #^"ACLID,deny|permit,IP,WM;ACLID,deny|permit,IP,SM;ACLID,IP,WM"
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
        """
        Writes the ACL configuration to the config file
        """
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        if(len(aclLines) > 0):
            self.configEditor.removeContentBetweenIndexes(aclLines[0], aclLines[-1])
        self.configEditor.appendContentToFile(aclConfig.toConfig())
        self.configEditor.writeConfig()


    #region NAT

    # Returns a NAT object with the NAT configuration in the config file
    def getNATConfig(self) -> NAT:
        """
        Returns a NAT object with the NAT configuration in the config file
        """
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        if len(natLines) == 0:
            return NAT("", "")
        natText = self.configEditor.getContentBetweenIndexes(natLines[0], natLines[-1])
        #^ip nat inside source list 1 interface Ethernet0/1 overload
        for line in natText:
            if line.startswith("ip nat inside source"):
                aclName = line.split(" ")[5]
                interfaceName = line.split(" ")[7]
            return NAT(interfaceName, aclName)

    # Writes the NAT configuration to the config file
    def writeNATConfig(self, natConfig: NAT) -> None:
        """
        Writes the NAT configuration to the config file
        """
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        if(len(natLines) > 0):
            self.configEditor.removeContentBetweenIndexes(natLines[0], natLines[-1])
        self.configEditor.appendContentToFile(natConfig.toConfig())
        self.configEditor.writeConfig()

    #endregion

    #region OSPF
    
    # returns a OSPF object that has the instanceID/processID from the input from the config file
    def getOSPFConfig(self, instanceName) -> OSPF:
        """
        Returns a OSPF object that has the instanceID/processID from the input from the config file
        """
        ospfLines = self.configEditor.findContentIndexes(f"router ospf {instanceName}", "!")
        ospfText = self.configEditor.getContentBetweenIndexes(ospfLines[0], ospfLines[-1])
        ospfProcessID = ospfText[0].split(" ")[2]
        #^router ospf 2
        ospfNetworks = ""
        ospfRouterID = ""
        ospfAutoSummary = False  
        ospfDefaultInformationOriginate = False

        for line in ospfText:
            if line.startswith("router-id"):
                #^ router-id 1.1.1.1
                ospfRouterID = line.split(" ")[1]
            elif line.startswith("default-information originate"):
                #^ default-information originate
                ospfDefaultInformationOriginate = True
            elif line.startswith("no auto-summary"):
                #^ no auto summary
                ospfAutoSummary = True #Danke Flo für des verkehrt denken
            elif line.startswith("network"):
                #^ network 192.168.1.0 0.0.0.255 area 0
                #^ network 192.168.2.0 0.0.0.255 area 0

                #check fi the ospfNetworks string is empty, if it is not, add a semicolon to separate the networks
                if len(ospfNetworks) > 0:
                    ospfNetworks += ";"
                ospfNetworks += line.split(" ")[1] + "," + line.split(" ")[2] + "," + line.split(" ")[4]

        return OSPF(ospfProcessID, ospfRouterID, ospfAutoSummary, ospfDefaultInformationOriginate, ospfNetworks)

    def getAllOSPFConfig(self) -> list[OSPF]:
        """
        Returns a list of OSPF objects with the OSPF configuration in the config file
        """
        ospfInstancesLines = self.configEditor.findMultipleContentIndexes("router ospf ")
        returnOspfObjects = []
        for ospfInstance in ospfInstancesLines:
            instanceID = self.configEditor.getContentOnIndex(ospfInstance[0]).split(" ")[2]
            returnOspfObjects.append(self.getOSPFConfig(instanceID))
        return returnOspfObjects


    #writes the OSPF config to the config file, replaces the OSPF configuration with the same processID
    def writeOSPFConfig(self, ospfConfig: OSPF) -> None:
        """
        Writes the OSPF config to the config file, replaces the OSPF configuration with the same processID
        """
        ospfLines = self.configEditor.findContentIndexes(f"router ospf {ospfConfig.ospfProcess}", "!")
        #check fi ospfLines is not empty, if it is, remove the content between the indexes
        if(len(ospfLines) > 0):
            self.configEditor.removeContentBetweenIndexes(ospfLines[0], ospfLines[-1])
        self.configEditor.appendContentToFile(ospfConfig.toConfig())
        self.configEditor.writeConfig()

    #endregion



    #region ExtendedACL

    def getExtendedACLConfig(self, aclName) -> ACLExtended:
        """
        Returns a ACLExtended object with the ACL configuration in the config file
        It searches for the "ip access-list extended" keyword and reads the configuration
        It only returns the value of the ACL with the selected name
        """
        aclLines = self.configEditor.findContentIndexes(f"ip access-list extended {aclName}", "!")
        aclText = self.configEditor.getContentBetweenIndexes(aclLines[0], aclLines[-1])
        #^ ip access-list extended test2
        returnAclRulesStr = ""
        for line in aclText:
            if line.startswith("permit") or line.startswith("deny"):
                #^ permit tcp 1.1.1.0 0.0.0.255 2.2.2.0 0.0.0.0 eq 10
                if len(returnAclRulesStr) > 0:
                    returnAclRulesStr += ";"

                permitDeny, protocol, sourceIP, sourceWM, destIP, destWM, eq, port = line.split(" ")
                returnAclRulesStr += permitDeny + "," + protocol + "," + sourceIP + "," + sourceWM + "," + destIP + "," + destWM + "," + port
        return ACLExtended(returnAclRulesStr, aclName)
    
    def getAllACLConfig(self) -> list[ACLExtended]:
        """
        Returns a list of ACLExtended objects with the ACL configuration in the config file
        It searches for the "ip access-list extended" keyword, and then loops over the found ACLs and reads the configuration
        """
        aclLines = self.configEditor.findMultipleContentIndexes("ip access-list extended", "!")
        returnACLObjects = []
        for acl in aclLines:
            aclText = self.configEditor.getContentBetweenIndexes(acl[0], acl[-1])
            aclName = aclText[0].split(" ")[3]
            returnACLObjects.append(self.getExtendedACLConfig(aclName))
        return returnACLObjects

    
    def writeExtendedACLConfig(self, aclConfig: ACLExtended) -> None:
        """
        Writes the aclConfig to the config file
        If no acl with the same name was found, it creates a new one, if one was found, it replaces the old one
        """
        aclLines = self.configEditor.findContentIndexes(f"ip access-list extended {aclConfig.aclRuleName}", "!")
        #^ ip access-list extended test2
        if(len(aclLines) > 0):
            self.configEditor.removeContentBetweenIndexes(aclLines[0], aclLines[-1])
        self.configEditor.appendContentToFile(aclConfig.toConfig())
        self.configEditor.writeConfig()


    #endregion


# region ExampleUsage

# filePath = "./exampleConfig"
# outputPath = "./exampleConfigOut"
# cM = ConfigManager(filePath,outputPath)



# aclconfig = cM.getExtendedACLConfig("test")
# print(cM.writeExtendedACLConfig(aclconfig))


# acls = cM.getAllACLConfig()
# for acl in acls:
#     print(acl.toConfig())
#     cM.writeExtendedACLConfig(acl)

# ospf = cM.getAllOSPFConfig()
# for i in ospf:
#     print(i.toConfig())
#     i.ospfRouterID = "3.3.3.3"
#     i.ospfOriginate = False
#     i.ospfAutoSummary = True
#     cM.writeOSPFConfig(i)



# cM.getDeviceInfo()

# extendedConfig = cM.getExtendedACLConfig("test")
# print(extendedConfig.toConfig())
# cM.writeExtendedACLConfig(extendedConfig)



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
