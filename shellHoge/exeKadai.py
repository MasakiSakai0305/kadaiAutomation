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

def parseJsonAndGetInputCases(jugyoNum:int, kadaiNum: str) -> List[List[str]]:
    inputCasesList = []
    f = open("./json/{}kai.json".format(jugyoNum), "r")
    jsonDict = json.load(f)
    kadaiDict = jsonDict[kadaiNum]
    inputCases = kadaiDict["inputCases"]
    for inputCase in inputCases:
        #print(inputCase, inputCases[inputCase])
        inputCasesList.append(inputCases[inputCase]["input"])
    return inputCasesList

def executeExeFile(jugyoNum: int, kihonDict: dict, hattenDict: dict, execFiles: List[str]):
    path = "./kadaiPrograms/{}kai/exec/"
    print('\n\n以下の内容でテストを実行します.')
    print('テスト対象({}件):\n'.format(len(kihonDict) + len(hattenDict)))
	
    # print('テストケース({}件):\n'.format(len(argSet)) + str(argSet))

    for i in range(1, len(kihonDict)+1):
        print("基本課題{}: ".format(i) + str(kihonDict["kihon{}".format(i)]))
    for i in range(1, len(hattenDict)+1):
        print("発展課題{}: ".format(i) + str(hattenDict["hatten{}".format(i)]))

    for i, execFile in enumerate(execFiles):
        print('\n[{}/{}]*****{}*****'.format(i+1, len(execFiles), execFile))


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
    print(len(kihonDict))
    return kihonDict, hattenDict

if __name__ == "__main__":
    jugyoNum = 1
    path = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    files = os.listdir(path=path)
    execFiles = os.listdir(path="./kadaiPrograms/{}kai/exec/".format(jugyoNum))
    # compileError = compileAssignments(files)

    print(parseJsonAndGetInputCases(jugyoNum=1, kadaiNum="kihon1"))
    k,h=calcKihonAndHatten(kihonNum=2, hattenNum=0, execFiles=execFiles)
    executeExeFile(jugyoNum=1,kihonDict=k, hattenDict=h, execFiles=execFiles)