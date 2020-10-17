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

def compileAssignments(specificFiles: List[str], jugyoNum: int) -> List[str]:
    print('\n*****コンパイル状況*****\n')
    compileError = []
    #logFilePath = "./kadaiPrograms/{}kai/kadaiCheckLog.csv".format(jugyoNum)
    print("未チェックの課題:\n{}".format(specificFiles) + "\n")

    for i, file in enumerate(specificFiles):
        # print("file:{}".format(file))
        p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(1) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    # inputCasesDict[kadaiNum] = []
    f = open("./json/{}kai.json".format(jugyoNum), "r")
    jsonDict = json.load(f)

    for kadaiNum in jsonDict:
        inputCasesDict[kadaiNum] = []
        inputCases = jsonDict[kadaiNum]["inputCases"]
        for inputCase in inputCases:
            inputCasesDict[kadaiNum].append(inputCases[inputCase]["input"])
    # print("inputCasesDict:{}".format(inputCasesDict))
    return inputCasesDict

def executeExeFileAndCheckAnswer(jugyoNum: int, kihonDict: dict, hattenDict: dict, execFiles: List[str]):
    exePath = "./kadaiPrograms/{}kai/exec/".format(jugyoNum)
    codesPath = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    print('\n\n以下の内容でテストを実行します.')
    print('テスト対象({}件):\n'.format(len(execFiles)))
	
    # print('テストケース({}件):\n'.format(len(argSet)) + str(argSet))
    
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
        execKadaiNum = execFile[:5]+execFile[7]
        #print("execFile:{}".format(execFile))
        print("実行入力ケース\n" + str(inputCasesDict[execKadaiNum]))
        #print("answers:{}".format(answerDict[execKadaiNum]))
        
        for inputCase in inputCasesDict[execKadaiNum]:
            
            p = subprocess.Popen([exePath + execFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            strArgs = '\n'.join(inputCase)
            o, e = p.communicate(input=strArgs.encode())
            print(o.decode())
            # print(type(o.decode()),o.decode()[:5])
            outputResults.append(o.decode())
            checkPoint = parseJsonAndGetCheckPoint(jugyoNum=jugyoNum, kadaiNum=execKadaiNum)
        
        if checkPoint == "figure":
            result, incorrectResult = checkKadai(outputResults=outputResults, studentID=execFile[-7:], answer=answerDict[execKadaiNum], kadaiNum=execKadaiNum)
        elif checkPoint == "string":
            result, incorrectResult = checkKadaiString(outputResults=outputResults, studentID=execFile[-7:], answer=answerDict[execKadaiNum], kadaiNum=execKadaiNum)

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

def calcKihonAndHatten(kihonNum: int, hattenNum: int, execFiles: List[str]):
    kihonDict={}
    hattenDict={}
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
    jugyoNum = 1
    path = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    lsitdir = os.listdir(path=path)
    files = [f for f in lsitdir if os.path.isfile(os.path.join(path, f))]
    #print("files:{}".format(files))
    compileError = compileAssignments(specificFiles=files, jugyoNum=jugyoNum)

    lsitdir = os.listdir(path="./kadaiPrograms/{}kai/exec/".format(jugyoNum))
    execFiles = [f for f in lsitdir if os.path.isfile(os.path.join("./kadaiPrograms/{}kai/exec/".format(jugyoNum), f))]
    #print("execFiles:{}".format(execFiles))
    
    parseJsonAndGetInputCases(jugyoNum=1)
    k,h=calcKihonAndHatten(kihonNum=2, hattenNum=0, execFiles=execFiles)
    executeExeFileAndCheckAnswer(jugyoNum=1,kihonDict=k, hattenDict=h, execFiles=execFiles)

    print('\n*****コンパイルエラー*****\n')
    for error in compileError:
        print("エラー対象:{}".format(error[0]))
        print("エラー内容:\n{}".format(error[1]))
