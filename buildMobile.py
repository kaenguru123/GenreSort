def getController():
    with open("./source/Controller.py") as f:
        content = ""
        while True:
            line = f.readline()
            if not line:
                break

            if line == "from Model import Model\n":
                content += getFileContent("./source/Model.py")
            else:
                content += line
        return f"\n# Controller.py\n" + content

def getFileContent(path):
    with open(path, "r") as f:
        return f"\n# {path}\n" + f.read()

with open("./source/View.py", "r") as f:
    buildedFileContent = ""
    while True:
        line = f.readline()
        if not line:
            break
        
        if line == "from Controller import Controller\n":
            buildedFileContent += getController()
        elif line == "from FileView import FileView\n":
            buildedFileContent += getFileContent("./source/FileView.py")
        elif line == "from GenreSort import GenreSort\n":
            buildedFileContent += getFileContent("./source/GenreSort.py")
        elif line == "from MusicPlayer import MusicPlayer\n":
            buildedFileContent += getFileContent("./source/MusicPlayer.py")
        else:
            buildedFileContent += line

    with open("./source/MobileView.py", "w") as f:
        f.write(buildedFileContent)
        