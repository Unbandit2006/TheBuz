def ReadConfigFile(filename:str):
    FileContent = []
    with open(filename, "r") as file:
        FileLines = file.readlines()
        for Line in FileLines:
            Line = Line.removesuffix("\n")

            if Line.__contains__(":"):
                Line = Line.split(":")
            
            FileContent.append(Line)

    return FileContent

if __name__ == '__main__':
    print(ReadConfigFile("C:\Dev\Messaging\ModernCode\Library\.config"))