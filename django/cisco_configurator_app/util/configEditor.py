import os
class configEditor:
    def __init__(self, filePath: str, outputPath: str = None):

        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the file path
        self.outputPath = outputPath if outputPath != None else filePath
        self.filePath = os.path.join(script_dir, filePath)
        self.outputPath = os.path.join(script_dir, self.outputPath)
        self.fileContent, self.fileLength = self.readFile()


    # Reads the input file and returns the content and length of the file
    def readFile(self) -> tuple[list, int]:
        """
        Reads the input file and returns the content and length of the file\n
        Returns a tuple with the content and length of the file\n
        """
        with open(self.filePath, "r") as configFile:
            content = configFile.readlines()
            fileLength = len(content)
        return content, fileLength


    # This function takes a config in the form of a list of lines and writes it to a fil
    def writeConfig(self) -> None:
        """
        Writes the internal config to the file\n
        """
        outputPath = self.outputPath
        with open(outputPath, 'w')as outputFile:  # write the file
            outputFile.writelines(self.fileContent)

    # This function takes a string and finds the index of the first line that starts with that string
    # It only gets the first one, and the endsWith parameter is optional and selects until when the content should be read
    def findContentIndexes(self, startsWith: str, endsWith: str = "!") -> list:
        """
        Returns a list of indexes of the content that starts with the given string until endsWith is reached\n
        The endsWith parameter is optional and selects until when the content should be read, defaults to "!"\n
        Uppercase and lowercase are irrelevant\n
        `[1,2,3,4,5,6,7]`
        """
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
        """
        This function finds startsWith and returns the indexes of the content that starts with the given string until endsWith is reached\n
        The endsWith parameter is optional and selects until when the content should be read, defaults to "!"\n
        It returns a list of lists with the indexes of the found content\n
        Uppercase and lowercase are irrelevant\n
        `[[1,2,3,4,5,6,7], [8,9,10,11,12,13,14]]`
        """
        self.fileContent, self.fileLength = self.readFile()
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
        """
        Returns the content between the start and end index as a list of strings:\n
        `["line1", "line2", "line3"]`
        """
        content = self.fileContent[startIndex:endIndex+1]
        returnContent = []
        for line in content:
            line = line.replace("\n", "") # Remove newline characters
            line = line.lstrip()    # Remove leading whitespace
            returnContent.append(line)
        return returnContent
    
    def getContentOnIndex(self, index: int) -> str:
        """
        Returns the content on the index as a string:\n
        `"line1"`
        """
        return self.fileContent[index].replace("\n", "").lstrip()


    def removeContentBetweenIndexes(self, startIndex: int, endIndex: int) -> None:
        """
        Removes the content between the start and end index\n
        Returns no value\n
        """
        self.fileContent = self.fileContent[:startIndex] + self.fileContent[endIndex+1:]

    def removeContentOnIndex(self, index: int) -> None:
        """
        Removes the content on the index\n
        Useful if you only have a single line to remove (like with a banner)\n
        Returns no value
        """
        self.fileContent = self.fileContent.pop(index)

    def appendContentToFile(self, content: list) -> list:
        """
        Appends content to the end of the file\n
        Returns no value\n
        """
        # self.fileContent, self.fileLength = self.readFile()
        self.fileContent = self.fileContent[:-1] + content + self.fileContent[-1:]



#Notes for documentation
# Order of Config?
# Why was code appended to the end of the file?

