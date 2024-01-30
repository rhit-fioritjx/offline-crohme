import shutil
import glob
import os
import inkml2img
from datetime import datetime
import re

dataPath = './offline-crohme/CROHME_labeled_2016/'
dataMergedPath = 'data_merged/'
targetFolder = 'data_processed/'
logger = open('log.txt', 'w+')
    
def writeLog(message):
    logger.write("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + str(message) + "\n")

def createDirectory(dirPath):
    if not os.path.exists(dirPath): 
        os.mkdir(dirPath)
        writeLog("Create " + dirPath)

if __name__ == "__main__":
    # pattern = re.compile(r"(\(|\$|[0-9]|(\\cdot)|(\\div)|(\\sin)|(\\cos)|(\\tan)|(\\times)|(\\(t|T)heta)|(\\(p|P)i)|(\\(d|D)elta)|=|\+|\-|\*|\/| |\)|[a-z]|[A-Z]|\.)*")
    # writeLog("Start processing.")
    # filesPath = glob.glob(dataPath + '*/*.inkml')
    # writeLog("There are " + str(len(filesPath)) + " files in " + dataPath)
    # createDirectory(dataMergedPath)

    # cnt = 0
    # for fileName in filesPath:
    #     cnt = cnt + 1
    #     print("Copying %d/%d" % (cnt, len(filesPath)))
    #     writeLog("Copied " + fileName + " --> " + dataMergedPath + fileName)
    #     shutil.copy2(fileName, dataMergedPath)

    createDirectory(targetFolder)

    listFiles = glob.glob(dataMergedPath + '*.inkml')
    numberOfFile = len(listFiles)
    writeLog("There are " + str(numberOfFile) + " files in " + dataMergedPath)
    cnt = 0

    for fileInkml in listFiles[:10]:
        cnt = cnt + 1
        fileName = fileInkml.split('\\')[-1]
        print("Processing %s [%d/%d]" % (fileName, cnt, numberOfFile))
        writeLog("[" + str(cnt) + "/" + str(numberOfFile) + "]" + "Processed " + fileInkml + " --> " + targetFolder + fileName + ".png")
        try:
            inkml2img.extract_symbols(fileInkml,targetFolder,fileName+'.jpg')
            # latex = inkml2img.get_label(fileInkml)
            # if re.fullmatch(pattern=pattern,string=latex) is not None:
            #     print("accepted:", latex)
            #     inkml2img.inkml2img(fileInkml, targetFolder + fileName + '.png')
            # else:
            #     print("rejected:", latex)
        except:
            writeLog("Failed!")
            print("An error occured!")

        writeLog("Successful!")

