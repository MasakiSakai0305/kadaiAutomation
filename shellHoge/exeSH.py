import subprocess
import re
from typing import List

# print(subprocess.call(['cat', 'hello.py'])) # 0
# # 標準入力・標準出力を指定する（2つ目はhello2.pyが作成される）
# print(subprocess.call(['cat'], stdin=open('hello.py','rb'))) # 0

"""
実行ファイルを実行できない(コンパイルエラーorそもそも.cファイルがない)とき，プログラムそのものがエラーになり，全ての出力結果を取得できなくなる
結論：shファイルから出力結果を得て，採点を自動化したいなら，学生一人毎の問題ごとのshファイルが必要になる．
例；一班10人，問題が４つ → 40個の.shが必要になる
"""
print(subprocess.check_output("./hoge.sh"))
print(type(subprocess.check_output("./hoge.sh")))
decoded = subprocess.check_output("./hoge.sh").decode("utf-8")
print(decoded, type(decoded))
print(decoded.split())
print(re.findall(r'\d+', decoded))


def exeKadai() -> (List[str], str):
    shFile = "hoge.sh"

    #shファイル出力結果
    outputResult = subprocess.check_output("./{}".format(shFile)).decode("utf-8").split()
    
    studentID = outputResult.pop(-1)
    #print("outputResult:{}".format(outputResult))
    return outputResult, studentID

def checkKadai(checkList: List[str], studentID: str,  answer: List[str]):
    ok = True
    responseList = []
    answerList = []
    checkPointList = []
    for check in checkList:
        checkPoint = re.findall(r'\d+', check)
 
        if checkPoint != answer:
            ok = False
            responseList.append(check)
            answerList.append(answer)
            checkPointList.append(checkPoint)

    
    if ok:
        print("学籍番号{}:正解".format(studentID))
    else:
        print("学籍番号{}:不正解\n".format(studentID))
        for i in range(len(responseList)):
            print("実行結果:{}".format(responseList[i]))
            print("チェックポイント:{}".format(checkPointList[i]))
            print("正解の実行結果：{}\n".format(answerList[i]))

def checkKadaiString(check: List[str], answer: List[str]):
    
    if answer in check:
        print("OK")
    else:
        print("NG")
        print("実行結果:{}".format(check))
        print("正解：{}".format(answer))


if __name__ == "__main__":
    answer = ["2", "2"]
    checkList, studentID = exeKadai()
    checkKadai(checkList, studentID, answer)
    #checkKadaiString(exeKadai(), "閏年です")