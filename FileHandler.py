import os


class FileHandler:
    def __init__(self):
        # PATH Configuration for the population to load and export data (need to add generalization features)
        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_FOLDER_PATH = os.path.join(self.BASE_PATH, "DATA/")

        self.PATHS = {
            
        }

        self.addPath("setting", "setting")

    def addPath(self, key, path):
        self.PATHS[key] = os.path.join(self.DATA_FOLDER_PATH, ((path)+".txt"))

    def readFileToArray(self, path):
        fileContents = []
        with open(self.PATHS[path], "r") as f:
            fileContents = f.readlines()
        
        return fileContents

    def exportToPath(self, path, population):
        for members in range(len(population)):
            current_member = population[members]
            
            try:
                with open(self.PATHS[path], "a+") as f:
                    f.write(str(current_member.exportGeneToArray()) + "\n")
                    f.flush()
            except KeyError:
                self.addPath(path, path)


    def recordArrayTo(self, array, file):
        with open(file, "a+") as f:
            for itm in range(len(array)):
                f.write(str(array[itm] + '\n'))