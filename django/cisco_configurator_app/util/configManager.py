from configEditor import configEditor
from deviceClasses import Interface, StaticRoute, RipRouting, DHCP, ACLStandard, NAT

filePath = "./exampleConfig.txt"
class ConfigManager:
    def __init__(self, configFilePath:str) -> None:
        self.filePath = configFilePath
        self.configEditor = configEditor(configFilePath)

        #region Interfaces

    def getAllInterfaces(self) -> list[Interface]:
        InterfacesLines = self.configEditor.findMultipleContentIndexes("interface ")
        returnInterfaceObjects = []
        print(InterfacesLines)
        for interfaceIndexes in InterfacesLines:
            interfaceText = self.configEditor.getContentOnIndex(interfaceIndexes[0])
            intName = interfaceText.split(" ")[1]

            returnInterfaceObjects.append(self.getInterface(intName))
        return returnInterfaceObjects

    def getInterface(self, interfaceName: str) -> Interface:
        InterfaceLines = self.configEditor.findContentIndexes("interface " + interfaceName, "!") #Finds the indexes of the interface in the config list
        interfaceText = self.configEditor.getContentBetweenIndexes(InterfaceLines[0], InterfaceLines[-1])
        intName, ip, sm, desc, natInside, natOutside, shut = None, None, None, "Default", None, None, True
        for intLine in interfaceText: #Iterates over the lines of the interface
            if intLine.startswith("interface "):
                intName = intLine.split(" ")[1]
            elif intLine.startswith("ip address"):
                ip = intLine.split(" ")[2]
                sm = intLine.split(" ")[3]
            elif intLine.startswith("ip nat"):
                nat = intLine.split(" ")[2]
                natInside = True if nat == "inside" else False
                natOutside = True if nat == "outside" else False
            elif intLine.startswith("description"):
                desc = intLine.split(" ")[1]
            elif intLine.startswith("shutdown") or intLine.startswith("no shutdown"):
                shut = False if intLine == "shutdown" else True
            if natInside == None: natInside = False
            if natOutside == None: natOutside = False
        return Interface(intName, ip, sm, natInside, natOutside, desc, shut)
    
    def writeInterface(self, interface: Interface) -> None:
        interfaceLines = self.configEditor.findContentIndexes("interface " + interface.interface, "!")
        self.configEditor.removeContentBetweenIndexes(interfaceLines[0], interfaceLines[-1])
        self.configEditor.appendContentToFile(interface.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region Static Routes


    def getStaticRoutes(self) -> StaticRoute:
        staticRoutesLines = self.configEditor.findContentIndexes("ip route ")
        returnStaticRoutes = ""
        for routeIndex in staticRoutesLines:
            routeText = self.configEditor.getContentOnIndex(routeIndex).split(" ")
            targetNw = routeText[2]
            targetSm = routeText[3]
            nextHop = routeText[4]
            if len(returnStaticRoutes) > 0:
                returnStaticRoutes += ";"
            returnStaticRoutes += targetNw + "," + targetSm + "," + nextHop
        return StaticRoute(returnStaticRoutes)
    
    def writeStaticRoutes(self, staticRoutes: StaticRoute) -> None:
        staticRouteLines = self.configEditor.findContentIndexes("ip route ")
        self.configEditor.removeContentBetweenIndexes(staticRouteLines[0], staticRouteLines[-1])
        self.configEditor.appendContentToFile(staticRoutes.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region RIP

    def getRIPConfig(self) -> RipRouting:
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        ripText = self.configEditor.getContentBetweenIndexes(ripLines[0], ripLines[-1])
        ripNetworks = []
        ripVersion, ripSumState, ripOriginate, ripNetworks = None, False, False, ""
        for ripLine in ripText:
            if ripLine.startswith("version"):
                ripVersion = ripLine.split(" ")[1]
            elif ripLine.startswith("no-auto summary"):
                ripSumState = True
            elif ripLine.startswith("default-information originate"):
                ripOriginate = True
            elif ripLine.startswith("network"):
                if len(ripNetworks) > 0:
                    ripNetworks += ";"
                ripNetworks += ripLine.split(" ")[1]
            
        return RipRouting(ripVersion, ripSumState, ripOriginate, ripNetworks)
    
    def writeRIPConfig(self, ripConfig: RipRouting) -> None:
        ripLines = self.configEditor.findContentIndexes("router rip", "!")
        self.configEditor.removeContentBetweenIndexes(ripLines[0], ripLines[-1])
        self.configEditor.appendContentToFile(ripConfig.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region DHCP

    def getDhcpConfig(self, inputPoolName: str ) -> DHCP:
        dhcpLines = self.configEditor.findContentIndexes(f"ip dhcp pool {inputPoolName}", "!")
        dhcpText = self.configEditor.getContentBetweenIndexes(dhcpLines[0], dhcpLines[-1])
        excludedLines = self.configEditor.findContentIndexes("ip dhcp excluded-address", "!")
        excludedText = self.configEditor.getContentBetweenIndexes(excludedLines[0], excludedLines[-1])
        poolName, networkIP, networkSM, defaultRouter, dnsServer = None, None, None, None, None
        excludedNetworks = ""
        for line in dhcpText:
            if line.startswith("ip dhcp pool"):
                poolName = line.split(" ")[3]
            elif line.startswith("network"):
                networkIP = line.split(" ")[1]
                networkSM = line.split(" ")[2]
            elif line.startswith("default-router"):
                defaultRouter = line.split(" ")[1]
            elif line.startswith("dns-server"):
                dnsServer = line.split(" ")[1]

        for line in excludedText:
            if(len(excludedNetworks) > 0):
                excludedNetworks += ";"
            excludedNetworks += line.split(" ")[3] + "," + line.split(" ")[4]
        return DHCP(networkIP, networkSM, defaultRouter, dnsServer, excludedNetworks, poolName)

    def writeDhcpConfig(self, dhcpConfig: DHCP) -> None:
        dhcpLines = self.configEditor.findContentIndexes(f"ip dhcp pool {dhcpConfig.dhcpPoolName}", "!")
        excludedLines = self.configEditor.findContentIndexes("ip dhcp excluded-address", "!")
        self.configEditor.removeContentBetweenIndexes(dhcpLines[0], dhcpLines[-1])
        self.configEditor.removeContentBetweenIndexes(excludedLines[0], excludedLines[-1])
        self.configEditor.appendContentToFile(dhcpConfig.toConfig())
        self.configEditor.writeConfig()
    #endregion

    #region ACL

    def getACLConfig(self) -> ACLStandard:
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        aclText = self.configEditor.getContentBetweenIndexes(aclLines[0], aclLines[-1])
        ACLs = "" #"ACLID,deny|permit,IP,SM;ACLID,deny|permit,IP,SM;ACLID,IP,SM"
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
    
    def writeACLConfig(self, aclConfig: ACLStandard) -> None:
        aclLines = self.configEditor.findContentIndexes("access-list ", "!")
        self.configEditor.removeContentBetweenIndexes(aclLines[0], aclLines[-1])
        self.configEditor.appendContentToFile(aclConfig.toConfig())
        self.configEditor.writeConfig()


    #region NAT

    def getNATConfig(self) -> NAT:
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        natText = self.configEditor.getContentBetweenIndexes(natLines[0], natLines[-1])
        for line in natText:
            if line.startswith("ip nat inside source"):
                aclName = line.split(" ")[5]
                interfaceName = line.split(" ")[7]
            return NAT(interfaceName, aclName)
                
    def writeNATConfig(self, natConfig: NAT) -> None:
        natLines = self.configEditor.findContentIndexes("ip nat inside ", "!")
        self.configEditor.removeContentBetweenIndexes(natLines[0], natLines[-1])
        self.configEditor.appendContentToFile(natConfig.toConfig())
        self.configEditor.writeConfig()

    #endregion


cM = ConfigManager(filePath)


# region Example Usage


# print(cM.getAllInterfaces())
# for i in cM.getAllInterfaces():
#     print(i.toConfig())
#     cM.writeInterface(i)

# print(cM.getInterface("Fast"))

# print(cM.getStaticRoutes().toConfig())

# interface = cM.getInterface("FastEthernet0/1")
# interface.ip = '10.10.23.11'
# cM.writeInterface(interface)

# staticRoutes = cM.getStaticRoutes()
# cM.writeStaticRoutes(staticRoutes)

# print(cM.getRIPConfig().toConfig())

# print(cM.getDhcpConfig("172"))
# print(cM.getDhcpConfig("172").toConfig())
# dhcpConfig = cM.getDhcpConfig("172")
# cM.writeDhcpConfig(dhcpConfig, "172")

# ripConfig = cM.getRIPConfig()
# ripConfig.ripVersion = "1"
# cM.writeRIPConfig(ripConfig)

# print(cM.getACLConfig().toConfig())
# cM.writeACLConfig(cM.getACLConfig())

# natConfig = cM.getNATConfig()
# natConfig.accessList = "5"
# cM.writeNATConfig(natConfig)

#endregion