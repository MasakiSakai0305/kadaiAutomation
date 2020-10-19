import subprocess
import os
import json
from typing import List
import shutil

from exeSH import checkKadai
from exeSH import checkKadaiString
from exeSH import parseJsonAndGetAnswers
from exeSH import parseJsonAndGetCheckPoint

jugyoNum = 1
path = "./kadaiPrograms/{}kai".format(jugyoNum)

def decodeByteToStr(byte_list: list) -> list:
	return  [i.decode('utf8') for i in byte_list]

def compileCommand(jugyoNum: int, kadaiNum: str) -> subprocess.Popen:
    """
    コンパイルコマンドが違う場合の場合分けを行う
    """
    p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pass

def executeCommand(jugyoNum: int, kadaiNum: str, exePath: str, execFile: str) -> subprocess.Popen:
    """
    実行コマンドが違う場合の場合分けを行う
    """
    p = subprocess.Popen([exePath + execFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if jugyoNum == 4:
        if kadaiNum == "kihon1" or kadaiNum == "kihon2":
            p = subprocess.Popen([exePath + execFile], "<", "seiseki.txt", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif kadaiNum == "hatten1":
            p = subprocess.Popen([exePath + execFile], "<", "joho.bmp", ">", "joho2.bmp", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif kadaiNum == "hatten2":
            p = subprocess.Popen([exePath + execFile], "<", "c.txt", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("p.type():{}".format(type(p)))
    return p

def compileAssignments(specificFiles: List[str], jugyoNum: int) -> List[str]:
    print('\n*****コンパイル状況*****\n')
    compileError = []
    #logFilePath = "./kadaiPrograms/{}kai/kadaiCheckLog.csv".format(jugyoNum)
    print("未チェックの課題:\n{}".format(specificFiles) + "\n")

    for i, file in enumerate(specificFiles):
        # print("file:{}".format(file))
        p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.readlines()
        stderr = p.stderr.readlines()
        print('対象ファイル: {0} ({1}/{2})'.format(file, i+1, len(specificFiles)))
        print('return: {}'.format(p.wait()))
        print('stdout: {}'.format(''.join(decodeByteToStr(stdout))))
        print('stderr:\n{}'.format(''.join(decodeByteToStr(stderr))))
        if len(stderr) > 0:
            compileError.append([file.rstrip('.c'), ''.join(decodeByteToStr(stderr))])
            # os.remove('./kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.rstrip('.c'))
    return compileError

def parseJsonAndGetInputCases(jugyoNum:int) -> List[List[str]]:
    inputCasesDict = {}
    inputCasesDict["kihon"] = {}
    inputCasesDict["hatten"] = {}

    f = open("./json/{}kai.json".format(jugyoNum), "r")
    jsonDict = json.load(f)

    for kadaiNum in jsonDict["kihon"]:
        inputCasesDict["kihon"][kadaiNum] = []
        inputCases = jsonDict["kihon"][kadaiNum]["inputCases"]
        for inputCase in inputCases:
            inputCasesDict["kihon"][kadaiNum].append(inputCases[inputCase]["input"])

    for kadaiNum in jsonDict["hatten"]:
        inputCasesDict["hatten"][kadaiNum] = []
        inputCases = jsonDict["hatten"][kadaiNum]["inputCases"]
        for inputCase in inputCases:
            inputCasesDict["hatten"][kadaiNum].append(inputCases[inputCase]["input"])

    #print("inputCasesDict:{}".format(inputCasesDict))
    return inputCasesDict

def executeExeFileAndCheckAnswer(jugyoNum: int, kihonDict: dict, hattenDict: dict, execFiles: List[str]):
    exePath = "./kadaiPrograms/{}kai/exec/".format(jugyoNum)
    codesPath = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    print('\n\n以下の内容でテストを実行します.')
    print('テスト対象({}件):\n'.format(len(execFiles)))
	 
    for i in range(1, len(kihonDict)+1):
        print("基本課題{}: ".format(i) + str(kihonDict["kihon{}".format(i)]))
    for i in range(1, len(hattenDict)+1):
        print("発展課題{}: ".format(i) + str(hattenDict["hatten{}".format(i)]))
        
    
    inputCasesDict = parseJsonAndGetInputCases(jugyoNum=jugyoNum)
    answerDict = parseJsonAndGetAnswers(jugyoNum=jugyoNum)

    correctList = []
    incorrectList = []
    incorrectResultList = []
    for i, execFile in enumerate(execFiles):
        outputResults = []
        print('\n[{}/{}]*****{}*****'.format(i+1, len(execFiles), execFile))
        if execFile[0] == "k":
            execKadaiNum = execFile[:5]+execFile[7]
            kadaiSyurui = "kihon"
        else:
            execKadaiNum = execFile[:6]+execFile[8]
            kadaiSyurui = "hatten"
        #print("execFile:{}".format(execFile))
        print("実行入力ケース\n" + str(inputCasesDict[kadaiSyurui][execKadaiNum]))

        #print("answers:{}".format(answerDict[kadaiSyurui][execKadaiNum]))
        
        for inputCase in inputCasesDict[kadaiSyurui][execKadaiNum]:
            
            p = executeCommand(jugyoNum=jugyoNum, kadaiNum=execKadaiNum, exePath=exePath, execFile=execFile)
            #p = subprocess.Popen([exePath + execFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            strArgs = '\n'.join(inputCase)
            o, e = p.communicate(input=strArgs.encode())
            print(o.decode())
            # print(type(o.decode()),o.decode()[:5])
            outputResults.append(o.decode())
            checkPoint = parseJsonAndGetCheckPoint(jugyoNum=jugyoNum, kadaiNum=execKadaiNum)
        
        if checkPoint == "figure":
            result, incorrectResult = checkKadai(outputResults=outputResults, studentID=execFile[-7:], answer=answerDict[kadaiSyurui][execKadaiNum], kadaiNum=execKadaiNum)
        elif checkPoint == "string":
            result, incorrectResult = checkKadaiString(outputResults=outputResults, studentID=execFile[-7:], answer=answerDict[kadaiSyurui][execKadaiNum], kadaiNum=execKadaiNum)

        if result:
            correctList.append(execFile)
            shutil.move(exePath + execFile, exePath + "ok")
            shutil.move(codesPath + execFile+".c", codesPath + "ok")
        else:
            incorrectList.append(execFile)
            incorrectResultList.append(incorrectResult)
    print("\n*****正解*****\n" + str(correctList))
    print("\n*****不正解*****\n" + str(incorrectList))
    print("\n*****不正解出力ケース*****\n" + str(incorrectResultList))

def calcKihonAndHatten(jugyoNum: int,execFiles: List[str]):
    kihonDict={}
    hattenDict={}
    jsonPath = "./json/{}kai.json".format(jugyoNum)
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kihonNum = len(jsonDict["kihon"])
    hattenNum = len(jsonDict["hatten"])
    for i in range(1, kihonNum+1):
        kihonDict["kihon{}".format(i)]=[]
    for i in range(1, hattenNum+1):
        hattenDict["hatten{}".format(i)]=[]

    for execFile in execFiles:
        if "kihon" in execFile:
            kadaiNum = execFile.split("-")[1][0]
            kihonDict["kihon{}".format(kadaiNum)].append(execFile)
        if "hatten" in execFile:
            kadaiNum = execFile.split("-")[1][0]
            hattenDict["hatten{}".format(kadaiNum)].append(execFile)
    return kihonDict, hattenDict


if __name__ == "__main__":
    print("授業回を入力")
    jugyoNum = int(input())
    path = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    lsitdir = os.listdir(path=path)
    files = [f for f in lsitdir if os.path.isfile(os.path.join(path, f))]
    #print("files:{}".format(files))
    compileError = compileAssignments(specificFiles=files, jugyoNum=jugyoNum)

    lsitdir = os.listdir(path="./kadaiPrograms/{}kai/exec/".format(jugyoNum))
    execFiles = [f for f in lsitdir if os.path.isfile(os.path.join("./kadaiPrograms/{}kai/exec/".format(jugyoNum), f))]
    #print("execFiles:{}".format(execFiles))
    
    parseJsonAndGetInputCases(jugyoNum=jugyoNum)
    k,h=calcKihonAndHatten(jugyoNum=jugyoNum,execFiles=execFiles)
    executeExeFileAndCheckAnswer(jugyoNum=jugyoNum,kihonDict=k, hattenDict=h, execFiles=execFiles)

    print('\n*****コンパイルエラー*****\n')
    for error in compileError:
        print("エラー対象:{}".format(error[0]))
        print("エラー内容:\n{}".format(error[1]))
