import subprocess
import os
import json
from typing import List

jugyoNum = 1
path = "./kadaiPrograms/{}kai".format(jugyoNum)

def decodeByteToStr(byte_list: list) -> list:
	return  [i.decode('utf8') for i in byte_list]

def compileAssignments(specificFiles):
    print('\n*****コンパイル状況*****\n')
    compileError = []
    for i, file in enumerate(specificFiles):
        print("file:{}".format(file))
        p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format("1") + file , '-o', './kadaiPrograms/{}kai/exec/'.format(1) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = p.stdout.readlines()
        stderr = p.stderr.readlines()
        print('対象ファイル: {0} ({1}/{2})'.format(file, i+1, len(specificFiles)))
        print('return: {}'.format(p.wait()))
        print('stdout: {}'.format(''.join(decodeByteToStr(stdout))))
        print('stderr:\n{}'.format(''.join(decodeByteToStr(stderr))))
        if len(stderr) > 0:
            compileError.append([file.rstrip('.c'), ''.join(decodeByteToStr(stderr))])
            os.remove('./kadaiPrograms/{}kai/exec/'.format(1) + file.rstrip('.c'))
    return compileError

def parseJsonAndGetInputCases(jugyoNum:int) -> List[List[str]]:
    inputCasesDict = {}
    # inputCasesDict[kadaiNum] = []
    f = open("./json/{}kai.json".format(jugyoNum), "r")
    jsonDict = json.load(f)

    for kadaiNum in jsonDict:
        print(11, kadaiNum)
        inputCasesDict[kadaiNum] = []
        inputCases = jsonDict[kadaiNum]["inputCases"]
        for inputCase in inputCases:
            inputCasesDict[kadaiNum].append(inputCases[inputCase]["input"])
    print("inputCasesDict:{}".format(inputCasesDict))
    return inputCasesDict

def executeExeFileAndCheckAnswer(jugyoNum: int, kihonDict: dict, hattenDict: dict, execFiles: List[str]):
    path = "./kadaiPrograms/{}kai/exec/".format(jugyoNum)
    print('\n\n以下の内容でテストを実行します.')
    print('テスト対象({}件):\n'.format(len(kihonDict) + len(hattenDict)))
	
    # print('テストケース({}件):\n'.format(len(argSet)) + str(argSet))
    
    for i in range(1, len(kihonDict)+1):
        print("基本課題{}: ".format(i) + str(kihonDict["kihon{}".format(i)]))
        # kihonInputCasesList.append(parseJsonAndGetInputCases(jugyoNum=jugyoNum, kadaiNum="kihon{}".format(i)))
    for i in range(1, len(hattenDict)+1):
        print("発展課題{}: ".format(i) + str(hattenDict["hatten{}".format(i)]))
        # hattenInputCasesList.append(parseJsonAndGetInputCases(jugyoNum=jugyoNum, kadaiNum="hatten{}".format(i)))
    
    
    inputCasesDict = parseJsonAndGetInputCases(jugyoNum=jugyoNum)
    for i, execFile in enumerate(execFiles):
        print('\n[{}/{}]*****{}*****'.format(i+1, len(execFiles), execFile))
        execKadaiNum = execFile[:5]+execFile[7]
        print("execFile:{}".format(execFile))
        print("実行入力ケース\n" + str(inputCasesDict[execKadaiNum]))
        for inputCase in inputCasesDict[execKadaiNum]:
            
            p = subprocess.Popen([path + execFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            strArgs = '\n'.join(inputCase)
            o, e = p.communicate(input=strArgs.encode())
            print(o.decode())


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
    files = os.listdir(path=path)
    execFiles = os.listdir(path="./kadaiPrograms/{}kai/exec/".format(jugyoNum))
    # compileError = compileAssignments(files)

    parseJsonAndGetInputCases(jugyoNum=1)
    k,h=calcKihonAndHatten(kihonNum=2, hattenNum=0, execFiles=execFiles)
    executeExeFileAndCheckAnswer(jugyoNum=1,kihonDict=k, hattenDict=h, execFiles=execFiles)