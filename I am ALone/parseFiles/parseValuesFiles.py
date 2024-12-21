import FileParserPython as FilePP
import os, json, sys, http, requests

libFreeLHtml = {

   f'webF{i}' : {
       "javaScript" : "js",
       "index" : "html",
       "pythonParse" : "py",
       "jsonScript" : "json",
       "css" : "css",
       "phpParse" : "php",
       "dangerousTIme" : {
            "@!%^#$#^@^!%#^@!" : ".txt"
        }
   } for i in range(3, 5)

}

def parseListFor(
    pathF, libraryF, modulesReq=[],
     valuesParams={"remove" : False}
) :

    try :

        for lib in dict(libraryF) :

            pathFolder = os.path.join(str(
                                pathF
                            ), lib)

            if bool("dict" in str(type(libraryF[lib]))) :
                
                if not bool(os.path.exists(pathFolder)) :
                    os.mkdir(pathFolder)
                parseListFor(pathFolder, libraryF[lib])

            else :
                
                fileMode = FilePP.LoaderFile({
                    "name" : str(lib)[0:
                        -int(len(str(lib)))
                    ],
                    "typeof" : str(libraryF[lib]),
                    "pathof" : str(pathFolder),
                    "modeof" : ""
                }, True)

                if not bool(os.path.exists(
                    fileMode.fileProps["pathof"]+
                    fileMode.fileProps["name"]+
                    '.'+fileMode.fileProps["typeof"]
                )) :
                    fileMode.fileProps["modeof"] = "w+"
                else :
                    fileMode.fileProps["modeof"] = "r"

                modulesReq.append(
                    fileMode.selfLoadWith()
                )

                for modL in list(set(os.listdir(pathF))):
                    if bool(
                        modL[:modL.find(".")] != pathFolder.split("\\")[-1] and
                        modL[modL.find(".")+1:] != fileMode.fileProps["typeof"]
                    ) :
                        if bool(valuesParams["remove"]) :
                            try :
                                os.remove(pathF+'\\'+modL)
                            except Exception :
                                break
                        else :
                            break
        return modulesReq

    except :
        
        pass


modulesList = parseListFor(
    r"c:\Users\celin\PycharmProjects\pythonProject\FreeLHtml",
     libFreeLHtml, valuesParams={"remove" : False}
)

for modL in list(modulesList) :
    
    modOrigin = open(
        os.path.realpath(modL.name), "a"
    )
    
    #baseCOde of HTML

    if bool(modOrigin.name[
        modOrigin.name.find(".") + 1:] == "html") :

        if not bool(
            str(open(
                r"c:\Users\celin\PycharmProjects\pythonProject\FreeLHtml\DefaultHTML.txt", "r").read()
            ).replace(" ", "") in modL.read().replace(" ", "")
            or len(
                str(open(
                    os.path.realpath(modL.name), "r").read()
                ).replace(" ", "")
            )
        ) :
            modOrigin.write(
                str(str(open(
                    r"c:\Users\celin\PycharmProjects\pythonProject\FreeLHtml\DefaultHTML.txt", "r").read()
                ).strip())
            )

    modOrigin.close()
    modL.close()
