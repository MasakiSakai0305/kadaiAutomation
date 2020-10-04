import subprocess
import re
from typing import List
import json

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

#shファイルを実行して課題ファイル(.c)をコンパイル → 実行
def exeKadai(shFile: str) -> (List[str], str):

    #shファイル出力結果
    outputResult = subprocess.check_output("./{}".format(shFile)).decode("utf-8").split()
    
    studentID = outputResult.pop(-1)
    #print("outputResult:{}".format(outputResult))
    return outputResult, studentID

#出力結果の数字を確認して採点する
def checkKadai(outputResult: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str):
    ok = True
    responseList = []
    answerList = []
    checkPointList = []
    i=0
    for check in outputResult:
        checkPoint = re.findall(r'\d+', check)
        if checkPoint != answer[i]:
            ok = False
            responseList.append(check)
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
def checkKadaiString(outputResult: List[str], studentID: str,  answer: List[List[str]], kadaiNum: str):
    ok = True
    responseList = []
    answerList = []
    checkPointList = []

    for i in range(len(outputResult)):
        #print(answer[i][0], outputResults[i])
        if answer[i][0] not in outputResult[i]:
            ok = False
            responseList.append(check)
            answerList.append(answer[i])
            checkPointList.append(checkPoint)

    if ok:
        print("学籍番号{}, {}:正解".format(studentID, kadaiNum))
    else:
        print("学籍番号{}, {}:不正解\n不正解入力ケース数:{}\n".format(studentID, kadaiNum, len(responseList)))
        for i in range(len(responseList)):
            print("実行結果:{}".format(responseList[i]))
            print("チェックポイント:{}".format(checkPointList[i]))
            print("正解の実行結果：{}\n".format(answerList[i]))


def parseJsonAndGetAnswers(kadaiNum: str) -> List[List[int]]:
    answerList = []
    
    jsonPath = "inputCaseHoge.json"
    f = open(jsonPath, "r")
    jsonDict = json.load(f)
    kadaiDict = jsonDict[kadaiNum]
    
    for i in range(1, kadaiDict["numberOfInputCases"]+1):
        #print(kadaiDict["inputCases"]["inputCase{}".format(i)])
        answerList.append(kadaiDict["inputCases"]["inputCase{}".format(i)]["answer"])
    
    return answerList


if __name__ == "__main__":
    # answer = [["2", "2"], ["2", "4"]]
    answerList = parseJsonAndGetAnswers(kadaiNum = "kihon1")
    outputResult, studentID = exeKadai(shFile = "hoge.sh")
    checkKadai(outputResult=outputResult, studentID=studentID, answer=answerList, kadaiNum = "kihon1")

    answerList = parseJsonAndGetAnswers(kadaiNum = "kihon2")
    outputResult, studentID = exeKadai(shFile = "shHoge2.sh")
    print(outputResult, studentID, answerList)
    checkKadaiString(outputResult, studentID, answerList, kadaiNum = "kihon2")
    #checkKadaiString(exeKadai(), "閏年です")
    