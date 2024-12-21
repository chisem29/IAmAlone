import os

def parseSysProperties(pathString, dictFolder={}, lambdaFolder=[]) :

    for osDir in list(os.listdir(pathString)) :

        dictFolder[osDir.rsplit('.', 1)[0]] = (os.path.abspath(f'{pathString}\\{osDir}') if not lambdaFolder else lambdaFolder[0]
            (f'{pathString}\\{osDir}')) if bool(os.path.isfile(f'{pathString}\\{osDir}')) else dict({})

        try :
            parseSysProperties(
                f'{pathString}\\{osDir}', dictFolder[
            osDir.rsplit('.', 1)[0]], lambdaFolder)
        except : 
            pass

    return dictFolder
    
class LoaderFile : 
    def __init__(self, fileProps, typeMode=False) :
        
        if bool(typeMode) :
            self.fileProps = fileProps
    
    def selfLoadWith(self) :

        try :

            fileLoad = open(
                f'{self.fileProps["pathof"]}{self.fileProps["name"]}.{self.fileProps["typeof"]}'
            , self.fileProps["modeof"]
            )

        except FileNotFoundError :

            pass

        return fileLoad

