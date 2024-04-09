# filePath = "exampleConfig.txt"


# fileContent = []
# fileLength = 0





# fileContent, fileLength = readFile()
# writeConfig(fileContent)
# print(fileContent)
# print(fileLength)
# foundIndexes = findContentIndexes(
#     "interface FastEthernet0/0", fileContent=fileContent)
# print(foundIndexes)
# content = getContentBetweenIndexes(foundIndexes[0], foundIndexes[-1], fileContent)

# print(removeContentBetweenIndexes(foundIndexes[0], foundIndexes[-1], fileContent))
# returnContent = appendContentToFile(content, fileContent)
# print(returnContent)

class configEditor:
    def __init__(self, filePath: str):
        self.filePath = filePath
        
        self.fileContent, self.fileLength = self.readFile()
        


    # Reads the input file and returns the content and length of the file
    def readFile(self) -> tuple[list, int]:
        with open(self.filePath, "r") as configFile:
            content = configFile.readlines()
            fileLength = len(content)
        return content, fileLength


    # This function takes a config in the form of a list of lines and writes it to a fil
    def writeConfig(self, updatedContent: list) -> None:
        outputPath = self.filePath.split(".")  # Split the file name by the period
        for i in range(0, len(outputPath)): # check if we are at the end of the string before the file type addon (.txt)
            if (i < len(outputPath)-2):
                outputPath[i] += "." #add any periods that were in the string originally, except the last one (.txt)
            elif (i == len(outputPath)-2): # add Output to the name of the file name
                outputPath[i] += "Output."

        # join the list of strings into one string
        outputPath = ''.join(outputPath)

        with open(outputPath, 'w')as outputFile:  # write the file
            outputFile.writelines(updatedContent)


    def findContentIndexes(self, startsWith: str, endsWith: str = "!") -> list:
        foundIndexes = []
        foundTarget = False
        for i in range(0, self.fileLength):
            if self.fileContent[i].startswith(startsWith) and foundTarget == False:
                foundIndexes.append(i)
                foundTarget = True
            elif endsWith in self.fileContent[i] and foundTarget == True:
                return foundIndexes
            elif foundTarget == True:
                foundIndexes.append(i)
                
    def findMultipleContentIndexes(self, startsWith: str, endsWith: str = "!") -> list:
        foundIndexes = [] #list of lists with the indexes of the found content
        foundTarget = False
        currentFinds = [] #The indexes of the currently found content (indexes of E0/0)
        for i in range(0, self.fileLength):
            if self.fileContent[i].startswith(startsWith) and foundTarget == False:
                currentFinds.append(i)
                foundTarget = True
            elif endsWith in self.fileContent[i] and foundTarget == True:
                foundIndexes.append(currentFinds.copy())
                currentFinds.clear()
                foundTarget = False
            elif foundTarget == True:
                currentFinds.append(i)
        return foundIndexes


    def getContentBetweenIndexes(self, startIndex: int, endIndex: int) -> list:
        return self.fileContent[startIndex:endIndex+1]


    def removeContentBetweenIndexes(self, startIndex: int, endIndex: int, fileContent: list) -> list:
        return fileContent[:startIndex] + fileContent[endIndex+1:]


    def appendContentToFile(self, content: list, fileContent: list) -> list:
        return fileContent[:-1] + content + fileContent[-1:]



#Notes for documentation
# Order of Config?
# Why was code appended to the end of the file?
