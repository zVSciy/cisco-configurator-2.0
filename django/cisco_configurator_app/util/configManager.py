from configEditor import configEditor
from deviceClasses import interfaces

filePath = "./exampleConfig.txt"
class configManager:
    def __init__(self, configFilePath:str) -> None:
        self.filePath = configFilePath
        self.configEditor = configEditor(configFilePath)
    
    def getAllInterfaces(self):
        InterfacesLines = self.configEditor.findMultipleContentIndexes("interface ")
        returnInterfaceObjects = []
        print(InterfacesLines)
        for interfaceIndexes in InterfacesLines:
            print(interfaceIndexes)
            interfaceText = self.configEditor.getContentBetweenIndexes(interfaceIndexes[0], interfaceIndexes[-1])
            print(interfaceText)
            intName, ip, sm, desc, shut = None, None, None, None, None
            for intLine in interfaceText: #Iterates over the lines of the interface
                if intLine.startswith("interface "):
                    intName = intLine
                elif intLine.startswith("ip"):
                    




            #interface = interfaces(interface)
            #print(interface)

    def getInterface(self, interfaceName: str):
        InterfaceLines = self.configEditor.findContentIndexes("interface " + interfaceName, "!")
        print(InterfaceLines)


cM = configManager(filePath)

cM.getAllInterfaces()
