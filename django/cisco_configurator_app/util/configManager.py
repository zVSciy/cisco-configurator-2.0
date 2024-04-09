from configEditor import configEditor
from deviceClasses import interfaces, StaticRouting

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

    def getStaticRoutes(self) -> StaticRouting:
        staticRoutes = self.configEditor.findContentIndexes("ip route ")
        returnStaticRoutes = ""
        for routeIndex in staticRoutes:
            routeText = self.configEditor.getContentOnIndex(routeIndex).split(" ")
            targetNw = routeText[2]
            targetSm = routeText[3]
            nextHop = routeText[4]
            if len(returnStaticRoutes) > 0:
                returnStaticRoutes += ";"
            returnStaticRoutes += targetNw + "," + targetSm + "," + nextHop
        return StaticRouting(returnStaticRoutes)


cM = configManager(filePath)



# print(cM.getAllInterfaces())
# print(cM.getInterface("Fast"))
# print(cM.getStaticRoutes().toConfig())
