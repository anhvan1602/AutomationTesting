import os
from pathlib import Path
from Libraries.Config import Default

curDir = str(Path(__file__).parent)


def getSymbolPathByOS():
    res = "\\"
    if Default.deviceTypeID == "MacOS":
        res = "/"
    return res


def getArrayPath():
    return str(Path(__file__).parent).split(getSymbolPathByOS())


def getVal_BySplitChar_Index(input_str, index):
    return input_str.split(getSymbolPathByOS())[index]


def getNameProject():
    return getVal_BySplitChar_Index(curDir, len(getArrayPath()) - 3)


def getPathToProjectName():
    arrayPath = getArrayPath()
    projectName = getNameProject()
    index = arrayPath.index(projectName)
    result = ""
    i = 0
    while i <= index:
        if i == 0:
            result = os.path.join(arrayPath[i] + getSymbolPathByOS())
        else:
            result = os.path.join(result, arrayPath[i])
        i = i + 1
    return result


class BasePaths:
    def __init__(self):
        self.drivers = "Drivers"
        self.libraries = "Libraries"
        self.reports = "Reports"
        self.proName = "Web"
        self.datas = "Datas"

    def getPathToLibraries(self):
        pathToProject = getPathToProjectName()
        return os.path.join(pathToProject, self.libraries)

    def getPathToDrivers(self):
        pathToProject = getPathToProjectName()
        return os.path.join(pathToProject, self.drivers)

    def getPathToDatas(self):
        pathToProject = getPathToProjectName()
        return os.path.join(pathToProject, self.datas)

    def getPathToDatasByFileName(self, fileName):
        pathDatas = self.getPathToDatas()
        return os.path.join(pathDatas, fileName)

    def getPathReport(self):
        pathToProject = getPathToProjectName()
        return os.path.join(pathToProject, self.reports)
    def getPathReportForWeb(self):
        pathToProject = self.getPathReport()
        return os.path.join(pathToProject, self.proName)


if __name__ == "__main__":
    print(BasePaths().getPathReport())
