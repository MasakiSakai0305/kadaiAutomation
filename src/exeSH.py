import subprocess
import re
from typing import List
import json
import os

# print(subprocess.call(['cat', 'hello.py'])) # 0
# # 標準入力・標準出力を指定する（2つ目はhello2.pyが作成される）
# print(subprocess.call(['cat'], stdin=open('hello.py','rb'))) # 0

"""
実行ファイルを実行できない(コンパイルエラーorそもそも.cファイルがない)とき，プログラムそのものがエラーになり，全ての出力結果を取得できなくなる
結論：shファイルから出力結果を得て，採点を自動化したいなら，学生一人毎の問題ごとのshファイルが必要になる．
例；一班10人，問題が４つ → 40個の.shが必要になる
"""
# print(subprocess.check_output("./hoge.sh"))
# print(type(subprocess.check_output("./hoge.sh")))
# decoded = subprocess.check_output("./hoge.sh").decode("utf-8")
# print(decoded, type(decoded))
# print(decoded.split())
# print(re.findall(r'\d+', decoded))

#shファイルを実行して課題ファイル(.c)をコンパイル → 実行 → 出力結果取得
def executeKadaiAndGetOutputResult(shFile: str) -> (List[str]):
    """
    shファイルを実行し，出力結果を取得する
    shファイル実行にはsubprocessモジュールを使用

    args
        shFile: str
        shファイルの名前(.sh拡張子付き)

    returns
        outputResult: List[str]
    """

    #shファイル出力結果
    outputResult = subprocess.check_output("./{}".format(shFile)).decode("utf-8").split()
    # outputResultForCheck = []
    # for output in outputResult:
    #     if keyword in output:
    #         outputResultForCheck.append(output)

    # print("outputResult:{}".format(outputResultForCheck))
    # exit()
    return outputResult

#shファイルから学籍番号を取得
def getStudentID(filename: str) -> str:
    """
    shファイルから学籍番号を返す
    splitで区切った文字列の後ろ7文字を取得

    args
        filename: str
        shファイルの名前(.sh拡張子付き)

    return
        List[str]

    examaple
        入力引数: kihon1-1-AL20001.sh
        返り値: AL20001
    """

    return filename.split(".sh")[0][-7:]


#出力結果の数字を確認して採点する
def checkKadai(outputResults: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str, inputCases: str) -> bool:
    """
    出力結果から課題の正解・不正解を判定
    出力結果の数値を見て判定する

    args
        outputResults: List[str]
            shファイル出力結果，executeKadaiAndGetOutputResult関数から取得したもの

        studentID: str 
            学籍番号,getStudentID関数から取得したもの

        answer: List[List[str]]
            課題の正解の出力結果，parseJsonAndGetAnswers関数から取得
            課題ごとのanswerを持つ

        kadaiNum: str
            課題番号
            例：kihon1

    return
        bool
        正解:True, 不正解:False
    """
    inputCases = inputCases.split("\n")
    ok = True
    responseList = []
    answerList = []
    checkPointList = []
    incorrectResponseList = []
    incorrectInputCases = []
    
    for i, outputResult in enumerate(outputResults):
        checkPoint = re.findall(r'\d+', outputResult)
        responseList.append(outputResult)

        #answerと実行出力結果をチェック
        if checkPoint != answer[i]:
            ok = False
            incorrectResponseList.append(outputResult)
            incorrectInputCases.append(inputCases[i])
            answerList.append(answer[i])
            checkPointList.append(checkPoint)
            break
        
         #answerと実行出力結果をチェック
        for j in range(len(answer[i])):
            responseList.append(outputResult)
            if answer[i][j] not in outputResult:
                # print("不正解になったよ\n", inputCases[i], outputResult, "\n")
                ok = False
                incorrectResponseList.append(outputResult)
                answerList.append(answer[i])
                incorrectInputCases.append(inputCases[i])
                break
    
    if ok:
        print("学籍番号{}, {}:正解".format(studentID, kadaiNum))
        for i in range(len(inputCases)):
            print("**入力ケース[{}/{}]**".format(i+1, len(inputCases)))
            print("入力:{}".format(inputCases[i]))
            print("実行結果\n{}\n".format(responseList[i]))
        return True, None
    else:
        print("学籍番号{}, {}:不正解\n不正解入力ケース数:{}\n".format(studentID, kadaiNum, len(incorrectResponseList)))
        for i in range(len(incorrectResponseList)):
            print("**入力ケース[{}/{}]**".format(i+1, len(incorrectResponseList)))
            print("入力:{}".format(incorrectInputCases[i]))
            print("実行結果\n{}".format(incorrectResponseList[i]))
            print("正解の実行結果\n{}\n".format(answerList[i]))
        return False, [responseList, answerList]


#数字ではなく，出力結果の文字列を確認して採点する
def checkKadaiString(outputResults: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str, inputCases: List[str]) -> bool:
    """
    出力結果から課題の正解・不正解を判定
    出力結果の文字列を見て判定する

    args
        outputResults: List[str]
            shファイル出力結果，executeKadaiAndGetOutputResult関数から取得したもの

        studentID: str 
            学籍番号,getStudentID関数から取得したもの

        answer: List[List[str]]
            課題の正解の出力結果，parseJsonAndGetAnswers関数から取得
            課題ごとのanswerを持つ

        kadaiNum: str
            課題番号
            例：kihon1

    return
        bool
        正解:True, 不正解:False
    """
    
    ok = True
    responseList = []
    incorrectResponseList = []
    answerList = []
    incorrectInputCases = []
    # print("outputResults:{}".format(outputResults))
    
    for i, outputResult in enumerate(outputResults):
        #print("answer[i][0]:{}".format(answer[i]))
            
        #answerと実行出力結果をチェック
        for j in range(len(answer[i])):
            responseList.append(outputResult)
            if answer[i][j] not in outputResult:
                # print("不正解になったよ\n", inputCases[i], outputResult, "\n")
                ok = False
                incorrectResponseList.append(outputResult)
                answerList.append(answer[i])
                incorrectInputCases.append(inputCases[i])
                break
                
    # print("aa", inputCases)
    if ok:
        print("学籍番号{}, {}:正解".format(studentID, kadaiNum))
        for i in range(len(inputCases)):
            print("**入力ケース[{}/{}]**".format(i+1, len(inputCases)))
            print("入力:{}".format(inputCases[i]))
            print("実行結果\n{}\n".format(responseList[i]))
        return True, None
    else:
        print("学籍番号{}, {}:不正解\n不正解入力ケース数:{}\n".format(studentID, kadaiNum, len(incorrectResponseList)))
        for i in range(len(incorrectResponseList)):
            print("**入力ケース[{}/{}]**".format(i+1, len(incorrectResponseList)))
            print("入力:{}".format(incorrectInputCases[i]))
            print("実行結果\n{}".format(incorrectResponseList[i]))
            print("正解の実行結果\n{}\n".format(answerList[i]))
        return False, [incorrectResponseList, answerList]

def parseJsonAndGetAnswers(jugyoNum: int) -> dict:
    """
    jsonをパースして，正解の出力結果を取得

    args
        jsonPath: str
            jsonファイルのパス

        kadaiNum: str
            課題番号
            例：kihon1

    return
        answersDict: dict
            その回の全ての課題の正解出力を辞書型にして返す
            複数回実行ケースがあり，その分の正解の出力結果をリストに格納
    """
    answersDict = {}
    jsonPath = "./json/{}kai.json".format(jugyoNum)

    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    answersDict["kihon"] = {}
    answersDict["hatten"] = {}
    # print("基本課題の数:{}".format(len(jsonDict["kihon"])))
    # print("発展課題の数:{}".format(len(jsonDict["hatten"])))

    for kadaiNum in jsonDict["kihon"]:
        answersDict["kihon"][kadaiNum] = []
        inputCases = jsonDict["kihon"][kadaiNum]["inputCases"]
        for inputCase in inputCases:
            answersDict["kihon"][kadaiNum].append(inputCases[inputCase]["answer"])

    for kadaiNum in jsonDict["hatten"]:
        answersDict["hatten"][kadaiNum] = []
        inputCases = jsonDict["hatten"][kadaiNum]["inputCases"]
        for inputCase in inputCases:
            answersDict["hatten"][kadaiNum].append(inputCases[inputCase]["answer"])
    #print("answersDict:{}".format(answersDict))
    return answersDict

def parseJsonAndGetCheckPoint(kadaiNum: str, jugyoNum: int) -> str:
    """
    jsonをパースして，チェックポイントを取得する
    チェックポイントは，課題チェックの際の見るべきポイントを指す
    数字チェックや文字列チェックがあるのでその際の判定に用いる．
    exmple
        figure: 数値を見る
        string: 文字列を見る


    args
        jsonPath: str
            jsonファイルのパス

        kadaiNum: str
            課題番号
            例：kihon1

    return
        str
    """
    jsonPath = "./json/{}kai.json".format(jugyoNum)
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kadaiSyurui = kadaiNum[:-1]
    kadaiDict = jsonDict[kadaiSyurui][kadaiNum]

    return kadaiDict["checkPoint"]



if __name__ == "__main__":
    # answer = [["2", "2"], ["2", "4"]]
    # answerList = parseJsonAndGetAnswers(kadaiNum = "kihon1")
    # outputResult, studentID = exeKadai(shFile = "hoge.sh")
    # checkKadai(outputResult=outputResult, studentID=studentID, answer=answerList, kadaiNum = "kihon1")

    # answerList = parseJsonAndGetAnswers(kadaiNum = "kihon2")
    # outputResult, studentID = exeKadai(shFile = "shHoge2.sh")
    # print(outputResult, studentID, answerList)
    # checkKadaiString(outputResult, studentID, answerList, kadaiNum = "kihon2")
    #checkKadaiString(exeKadai(), "閏年です")
    
    
    answerList = parseJsonAndGetAnswers(jugyoNum=1)
    #os.chdir("scriptAndprogram/")

    outputResult = executeKadaiAndGetOutputResult(shFile = "kihon1-1-AL20024.sh")
    studentID = getStudentID(filename="kihon1-1-AL20024.sh")
    print(outputResult, studentID, answerList)
    checkKadai(outputResult=outputResult, studentID=studentID, answer=answerList, kadaiNum = "kihon1")
