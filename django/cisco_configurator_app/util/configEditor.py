import os
class configEditor:
    def __init__(self, filePath: str):
        self.filePath = filePath
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the file path
        self.filePath = os.path.join(script_dir, filePath)
        self.fileContent, self.fileLength = self.readFile()        


    # Reads the input file and returns the content and length of the file
    def readFile(self) -> tuple[list, int]:
        with open(self.filePath, "r") as configFile:
            content = configFile.readlines()
            fileLength = len(content)
        return content, fileLength


    # This function takes a config in the form of a list of lines and writes it to a fil
    def writeConfig(self) -> None:
        outputPath = self.filePath


        # outputPath = self.filePath.split(".")  # Split the file name by the period
        # for i in range(0, len(outputPath)): # check if we are at the end of the string before the file type addon (.txt)
        #     if (i < len(outputPath)-2):
        #         outputPath[i] += "." #add any periods that were in the string originally, except the last one (.txt)
        #     elif (i == len(outputPath)-2): # add Output to the name of the file name
        #         outputPath[i] += "Output."

        # # join the list of strings into one string
        # outputPath = ''.join(outputPath)

        with open(outputPath, 'w')as outputFile:  # write the file
            outputFile.writelines(self.fileContent)

    # This function takes a string and finds the index of the first line that starts with that string
    # It only gets the first one, and the endsWith parameter is optional and selects until when the content should be read
    def findContentIndexes(self, startsWith: str, endsWith: str = "!") -> list:
        foundIndexes = []
        foundTarget = False
        # for i in range(0, self.fileLength):
        for i, content in enumerate(self.fileContent):
            if content.lower().startswith(startsWith.lower()) and foundTarget == False:
                foundIndexes.append(i)
                foundTarget = True
            elif endsWith in content and foundTarget == True:
                return foundIndexes
            elif foundTarget == True:
                foundIndexes.append(i)
        return foundIndexes
                
    def findMultipleContentIndexes(self, startsWith: str, endsWith: str = "!") -> list:
        foundIndexes = [] #list of lists with the indexes of the found content
        foundTarget = False
        currentFinds = [] #The indexes of the currently found content (indexes of E0/0)
        # for i in range(0, self.fileLength):
        for i,content   in enumerate(self.fileContent):
            if content.lower().startswith(startsWith.lower()) and foundTarget == False:
                currentFinds.append(i)
                foundTarget = True
            elif endsWith in content and foundTarget == True:
                foundIndexes.append(currentFinds.copy())
                currentFinds.clear()
                foundTarget = False
            elif foundTarget == True:
                currentFinds.append(i)
        return foundIndexes


    def getContentBetweenIndexes(self, startIndex: int, endIndex: int) -> list:
        content = self.fileContent[startIndex:endIndex+1]
        returnContent = []
        for line in content:
            line = line.replace("\n", "") # Remove newline characters
            line = line.lstrip()    # Remove leading whitespace
            returnContent.append(line)
        return returnContent
    
    def getContentOnIndex(self, index: int) -> str:
        return self.fileContent[index].replace("\n", "").lstrip()


    def removeContentBetweenIndexes(self, startIndex: int, endIndex: int) -> None:
        self.fileContent = self.fileContent[:startIndex] + self.fileContent[endIndex+1:]


    def appendContentToFile(self, content: list) -> list:
        self.fileContent = self.fileContent[:-1] + content + self.fileContent[-1:]



#Notes for documentation
# Order of Config?
# Why was code appended to the end of the file?

