class FileHandler:
    def __init__(self):
        pass

    def recordArrayTo(self, array, file):
        with open(file, "a+") as f:
            for itm in range(len(array)):
                f.write(str(array[itm] + '\n'))