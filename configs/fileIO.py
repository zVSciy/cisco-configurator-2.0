filePath = "exampleConfig.txt"
fileContent = []
fileLength = 0


def readFile() -> list:
    with open(filePath, "r") as configFile:
        content = configFile.readlines()
        fileLength = len(content)
    return content, fileLength

def writeConfig(updatedContent: list) -> None:

    outputPath = filePath.split(".")
    for i in range(0, len(outputPath)):
        if(i < len(outputPath)-2):
            outputPath[i] += "."    
        elif (i == len(outputPath)-2):
            outputPath[i] += "Output."


    outputPath = ''.join(outputPath)

    with open(outputPath, 'w')as outputFile:
        outputFile.writelines(updatedContent)

def findContentIndexes(startsWith: str, endsWith:str = "!") -> list:
    foundIndexes = []
    foundTarget = False
    for i in range(0,fileLength):
        if fileContent[i].startswith(startsWith) and foundTarget == False:
            foundIndexes.append(i)
            foundTarget = True
        elif endsWith in fileContent[i]:
            return




fileContent, fileLength = readFile()
writeConfig(fileContent) 
print(fileContent)
print(fileLength)

