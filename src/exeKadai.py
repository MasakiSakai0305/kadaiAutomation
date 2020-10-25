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
    args
        jugyoNum:int
            授業の回(例：第4回の場合、jugyoNum=4)
        kadaiNum:str
            課題番号(例: "hatten1")
    return
        なし
    """
    p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pass

def executeCommand(jugyoNum: int, kadaiNum: str, exePath: str, execFile: str) -> subprocess.Popen:
    """
    実行コマンドが違う場合の場合分けを行う.
    txtファイルなどをコマンドに入れて使う課題があるため作成.
    例: 第4回基本課題1 -> [~~]$./a.out < aaa.txt
    実行に必要なファイルのパス: ./kadaiPrograms/4kai/codes/option/
    args
        jugyoNum:int
            授業の回(例：第4回の場合、jugyoNum=4)
        kadaiNum:str
            課題番号(例: "hatten1") 
        exePath: str
            課題実行ファイルのパス
            (exePath = "./kadaiPrograms/{}kai/exec/".format(jugyoNum))
        execFile: str
            課題の実行ファイル名(例: "kihon1-1-AL20000")
    return
        subprocess.Popen
        subprocessモジュールで課題実行を行ったときのオブジェクト
    """
    p = subprocess.Popen([exePath + execFile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if jugyoNum == 4:
        if kadaiNum == "kihon1" or kadaiNum == "kihon2":
            p = subprocess.Popen("{}{} < ./kadaiPrograms/4kai/codes/option/seiseki.txt".format(exePath, execFile),shell=True,  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #p = subprocess.Popen(['{}{}'.format(exePath, execFile), ' < ', ' ./kadaiPrograms/4kai/codes/option/seiseki.txt'],  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif kadaiNum == "hatten2":
            p = subprocess.Popen("{}{} < ./kadaiPrograms/4kai/codes/option/c.txt".format(exePath, execFile), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p

def compileAssignments(specificFiles: List[str], jugyoNum: int) -> List[str]:
    """
    課題をコンパイルするための関数.
    .cファイル名が格納された配列を受け取り, 順番に実行していく.
    args
        specificFiles: List[str]
            コンパイルされる前の.cファイル名(str)が格納されている配列
            例: ["kihon1-1-AL20000.c","kihon1-2-AL20000.c"]
        jugyoNum: int
            授業の回(例：第4回の場合、jugyoNum=4)
    return
        compileError: List[str]
        コンパイルエラーしたファイルと, エラーメッセージが配列に格納されている.
    """
    print('\n*****コンパイル状況*****\n')
    compileError = []
    #logFilePath = "./kadaiPrograms/{}kai/kadaiCheckLog.csv".format(jugyoNum)
    print("未チェックの課題:\n{}".format(specificFiles) + "\n")

    for i, file in enumerate(specificFiles):
        # print("file:{}".format(file))
        p = subprocess.Popen(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.replace('.c', '')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(['gcc', './kadaiPrograms/{}kai/codes/'.format(jugyoNum) + file , '-o', './kadaiPrograms/{}kai/exec/'.format(jugyoNum) + file.replace('.c', '')])
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

def parseJsonAndGetInputCases(jugyoNum:int) -> dict:
    """
    [n]kai.jsonをパースし, その回の入力ケースを返す関数.
    基本と発展も両方を一つの変数にまとめて返す.
    args
        jugyoNum: int
            授業の回(例：第4回の場合、jugyoNum=4)
    return
        inputCasesDict: dict
        例: {'hatten': {'hatten2': [['']], 'hatten3': [['4', '3', '2', '1', '1', '1', '1', '1'], ['1', '2', '3', '4', '1', '1', '1', '1']]}, 
        'kihon': {'kihon1': [['']], 'kihon2': [['']]}}
        課題ごとに入力ケースを配列に格納している.一回の実行で複数入力が行われる場合は, 1つのリストに複数の文字列が格納される.
        dict型のため, 課題の並び順は考慮しない.
    """
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

    # print("inputCasesDict:{}".format(inputCasesDict))
    return inputCasesDict

def executeExeFileAndCheckAnswer(jugyoNum: int, kihonDict: dict, hattenDict: dict, execFiles: List[str]):
    """
    コンパイルされた実行ファイルを実行し, 正解か不正解かを判定する関数.
    判定は, 実行した出力結果と, 実際の正解の出力結果を照合して行う.
    入力ケースはparseJsonAndGetInputCases関数を用いて取得, 
    正解の出力結果はparseJsonAndGetAnswers関数(from exeSH.py)を用いて取得,
    正解・不正解の判定はcheckKadai関数(from exeSH.py)で行う.
    判定の関数は二つあり, checkKadai(判定するのは数字), checkKadaiString(判定するのは文字列)である.
    args
        jugyoNum: int
            授業の回(例：第4回の場合、jugyoNum=4)
        kihonDict: dict
            課題ごとの, 実行する実行ファイルのファイル名を格納した配列をdictにさらに格納している.
            課題を実行する前に, どのファイルを実行するのかを課題ごとに表示するために使用.
            例: {'kihon2': ["kihon1-2-AL20000"], 'kihon1': ["kihon1-1-AL20000"]}
        hattenDict: dict
            kihonDictの発展課題ver.
        execFiles: List[str]
            課題の実行ファイル名を配列に格納したもの(例: ["kihon1-1-AL20000"])    
    return
        なし
    関数内で使用する主な変数(後から見直したら分からなくなりそうなので記述)
        outputResults: List[str]
            プログラムの出力結果が配列に格納されている.
            答えに関係するところ以外の出力も格納されている.
        checkPoint: str
            [n]kai.jsonをパースしたときに得られる変数.
            checkKadai関数, checkKadaiString関数のどちらを使うを判別するときに使用.
    """
    exePath = "./kadaiPrograms/{}kai/exec/".format(jugyoNum)
    codesPath = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    print('\n\n以下の内容でテストを実行します.')
    print('テスト対象({}件):\n'.format(len(execFiles)))
    # print("kihonDict:{}\nhattendict:{}".format(kihonDict, hattenDict))
    print("execFiles:{}".format(execFiles))

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
            # print("outputResults:{}".format(outputResults))
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

def calcKihonAndHatten(jugyoNum: int,execFiles: List[str]) -> (dict, dict):
    """
    args
        jugyoNum: int
            授業の回(例：第4回の場合、jugyoNum=4)
        execFiles: List[str]
            課題の実行ファイル名を配列に格納したもの(例: ["kihon1-1-AL20000"])
    returns
        下記の2変数は, executeExeFileAndCheckAnswer関数内で, 確認用に使用する変数.
            kihonDict: dict
                課題ごとの, 実行する実行ファイルのファイル名を格納した配列をdictにさらに格納している.
                課題を実行する前に, どのファイルを実行するのかを課題ごとに表示するために使用.
                例: {'kihon2': ["kihon1-2-AL20000"], 'kihon1': ["kihon1-1-AL20000"]}
            hattenDict: dict
                kihonDictの発展課題ver.
    """
    kihonDict={}
    hattenDict={}
    jsonPath = "./json/{}kai.json".format(jugyoNum)
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kihonNum = len(jsonDict["kihon"])
    hattenNum = len(jsonDict["hatten"])
    for i in range(1, kihonNum+1):
        kihonDict["kihon{}".format(i)]=[]
    for i in range(1, hattenNum+2):
        hattenDict["hatten{}".format(i)]=[]

    for execFile in execFiles:
        if "kihon" in execFile:
            kadaiNum = execFile.split("-")[1][0]
            kihonDict["kihon{}".format(kadaiNum)].append(execFile)
        if "hatten" in execFile:
            kadaiNum = execFile.split("-")[1][0]
            hattenDict["hatten{}".format(kadaiNum)].append(execFile)
    print("hogeee", kihonDict, hattenDict)
    return kihonDict, hattenDict


if __name__ == "__main__":
    jugyoNum = int(input("授業回を入力:"))
    path = "./kadaiPrograms/{}kai/codes/".format(jugyoNum)
    lsitdir = os.listdir(path=path)

    #ファイルのパスのみを抽出(.cファイル)
    files = [f for f in lsitdir if os.path.isfile(os.path.join(path, f))]
    compileError = compileAssignments(specificFiles=files, jugyoNum=jugyoNum)
    lsitdir = os.listdir(path="./kadaiPrograms/{}kai/exec/".format(jugyoNum))
    #ファイルのパスのみを抽出(実行ファイル)
    execFiles = [f for f in lsitdir if os.path.isfile(os.path.join("./kadaiPrograms/{}kai/exec/".format(jugyoNum), f))]
    
    k,h=calcKihonAndHatten(jugyoNum=jugyoNum,execFiles=execFiles)
    executeExeFileAndCheckAnswer(jugyoNum=jugyoNum,kihonDict=k, hattenDict=h, execFiles=execFiles)

    print('\n*****コンパイルエラー*****\n')
    for error in compileError:
        print("エラー対象:{}".format(error[0]))
        print("エラー内容:\n{}".format(error[1]))
