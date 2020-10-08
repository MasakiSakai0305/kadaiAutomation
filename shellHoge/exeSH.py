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
    return filename.split(".sh")[0][-7:]


#出力結果の数字を確認して採点する
def checkKadai(outputResults: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str):
    ok = True
    responseList = []
    answerList = []
    checkPointList = []
    i=0
    for outputResult in outputResults:
        checkPoint = re.findall(r'\d+', outputResult)

        #answerと実行出力結果をチェック
        if checkPoint != answer[i]:
            ok = False
            responseList.append(outputResult)
            answerList.append(answer[i])
            checkPointList.append(checkPoint)
        i+=1
    
    if ok:
        print("学籍番号{}, {}:正解".format(studentID, kadaiNum))
    else:
        print("学籍番号{}, {}:不正解\n不正解入力ケース数:{}\n".format(studentID, kadaiNum, len(responseList)))
        for i in range(len(responseList)):
            print("実行結果:{}".format(responseList[i]))
            print("チェックポイント:{}".format(checkPointList[i]))
            print("正解の実行結果：{}\n".format(answerList[i]))


#数字ではなく，出力結果の文字列を確認して採点する
def checkKadaiString(outputResults: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str):
    ok = True
    responseList = []
    answerList = []
    i=0
    
    for outputResult in outputResults:
        
        #answerと実行出力結果をチェック
        if answer[i][0] not in outputResult:
            ok = False
            responseList.append(outputResult)
            answerList.append(answer[i])
            
        i+=1
    if ok:
        print("学籍番号{}, {}:正解".format(studentID, kadaiNum))
    else:
        print("学籍番号{}, {}:不正解\n不正解入力ケース数:{}\n".format(studentID, kadaiNum, len(responseList)))
        for i in range(len(responseList)):
            print("実行結果:{}".format(responseList[i]))
            print("正解の実行結果：{}\n".format(answerList[i]))


def parseJsonAndGetAnswers(jsonPath: str, kadaiNum: str) -> (List[List[int]]):
    answerList = []
    
    # jsonPath = "json/inputCaseHoge.json"
    #jsonPath = "json/1-1.json"

    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kadaiDict = jsonDict[kadaiNum]
    
    for i in range(1, kadaiDict["numberOfInputCases"]+1):
        #print(kadaiDict["inputCases"]["inputCase{}".format(i)])
        answerList.append(kadaiDict["inputCases"]["inputCase{}".format(i)]["answer"])
    
    return answerList

def parseJsonAndGetCheckPoint(jsonPath: str, kadaiNum: str) -> str:
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kadaiDict = jsonDict[kadaiNum]

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
    
    
    answerList = parseJsonAndGetAnswers(jsonPath="json/1-1.json",kadaiNum = "kihon1")
    os.chdir("scriptAndprogram/")

    outputResult = executeKadaiAndGetOutputResult(shFile = "kihon1-1-AL20024.sh")
    studentID = getStudentID(filename="kihon1-1-AL20024.sh")
    print(outputResult, studentID, answerList)
    checkKadai(outputResult=outputResult, studentID=studentID, answer=answerList, kadaiNum = "kihon1")
