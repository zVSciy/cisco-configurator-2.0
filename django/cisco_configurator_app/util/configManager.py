from configEditor import configEditor
from deviceClasses import interfaces, StaticRouting, ripRouting

filePath = "./exampleConfig.txt"
class configManager:
    def __init__(self, configFilePath:str) -> None:
        self.filePath = configFilePath
        self.configEditor = configEditor(configFilePath)
    
    def getAllInterfaces(self) -> list[interfaces]:
        InterfacesLines = self.configEditor.findMultipleContentIndexes("interface ")
        returnInterfaceObjects = []
        print(InterfacesLines)
        for interfaceIndexes in InterfacesLines:
            print(interfaceIndexes)
            interfaceText = self.configEditor.getContentBetweenIndexes(interfaceIndexes[0], interfaceIndexes[-1])
            print(interfaceText)
            intName, ip, sm, desc, shut = None, None, None, "Default", "no shutdown"
            for intLine in interfaceText: #Iterates over the lines of the interface
                if intLine.startswith("interface "):
                    intName = intLine.split(" ")[1]
                elif intLine.startswith("ip"):
                    ip = intLine.split(" ")[2]
                    sm = intLine.split(" ")[3]
                elif intLine.startswith("description"):
                    desc = intLine.split(" ")[1]
                elif intLine.startswith("shutdown") or intLine.startswith("no shutdown"):
                    shut = intLine
            returnInterfaceObjects.append(interfaces(intName, ip, sm, desc, shut))
        return returnInterfaceObjects

    def getInterface(self, interfaceName: str) -> interfaces:
        InterfaceLines = self.configEditor.findContentIndexes("interface " + interfaceName, "!")
        interfaceText = self.configEditor.getContentBetweenIndexes(InterfaceLines[0], InterfaceLines[-1])
        intName, ip, sm, desc, shut = None, None, None, "Default", "no shutdown"
        for intLine in interfaceText: #Iterates over the lines of the interface
            if intLine.startswith("interface "):
                intName = intLine.split(" ")[1]
            elif intLine.startswith("ip"):
                ip = intLine.split(" ")[2]
                sm = intLine.split(" ")[3]
            elif intLine.startswith("description"):
                desc = intLine.split(" ")[1]
            elif intLine.startswith("shutdown") or intLine.startswith("no shutdown"):
                shut = intLine
        return interfaces(intName, ip, sm, desc, shut)
    
    def writeInterface(self, interface: interfaces) -> None:
        interfaceLines = self.configEditor.findContentIndexes("interface " + interface.interface, "!")
        self.configEditor.removeContentBetweenIndexes(interfaceLines[0], interfaceLines[-1])
        self.configEditor.appendContentToFile(interface.toConfig())
        self.configEditor.writeConfig()

    def getStaticRoutes(self) -> StaticRouting:
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
        return StaticRouting(returnStaticRoutes)
    
    def writeStaticRoutes(self, staticRoutes: StaticRouting) -> None:
        staticRouteLines = self.configEditor.findContentIndexes("ip route ")
        self.configEditor.removeContentBetweenIndexes(staticRouteLines[0], staticRouteLines[-1])
        self.configEditor.appendContentToFile(staticRoutes.toConfig())
        self.configEditor.writeConfig()

    # def getRIPConfig(self) -> ripRouting:
    #     ripLines = self.configEditor.findContentIndexes("router rip", "!")
    #     ripText = self.configEditor.getContentBetweenIndexes(ripLines[0], ripLines[-1])
    #     ripNetworks = []
    #     for ripLine in ripText:
    #         if ripLine.startswith("network"):
    #             ripNetworks.append(ripLine.split(" ")[1])
    #     return ripRouting(ripNetworks)

cM = configManager(filePath)



# print(cM.getAllInterfaces())
# print(cM.getInterface("Fast"))
# print(cM.getStaticRoutes().toConfig())

# interface = cM.getInterface("FastEthernet0/1")
# interface.ip = '10.10.23.11'
# cM.writeInterface(interface)

staticRoutes = cM.getStaticRoutes()
cM.writeStaticRoutes(staticRoutes)