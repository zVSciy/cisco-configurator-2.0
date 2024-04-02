from configEditor import configEditor

filePath = "../../../configs/exampleConfig.txt"

# configEditor = configEditor(filePath)

# indexes = configEditor.findContentIndexes("interface FastEthernet0/0")

# indexess = configEditor.findMultipleContentIndexes("interface")

class configManager:
    def __init__(self, configFilePath:str) -> None:
        filePath = configFilePath
    