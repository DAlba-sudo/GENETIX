class FileHandler:
    def __init__(self):
        pass

    def elimFromString(self, elimChar, phrase):
        newString = ""
        for char in range(len(phrase)):
            current_char = phrase[char]
            if ((current_char) == ((elimChar))):
                pass
            else:
                newString += current_char
        
        return newString