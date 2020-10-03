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


def exeKadai() -> str:
    shFile = "hoge.sh"
    kaito = subprocess.check_output("./{}".format(shFile)).decode("utf-8")
    return kaito

def checkKadai(check: str, answer: List[str]):
    checkPoint = re.findall(r'\d+', check)
    if checkPoint == answer:
        print("OK")
    else:
        print("NG")
        print("実行結果:{}".format(check))
        print("正解：{}".format(answer))


def checkKadaiString(check: str, answer: List[str]):
    
    if answer in check:
        print("OK")
    else:
        print("NG")
        print("実行結果:{}".format(check))
        print("正解：{}".format(answer))


if __name__ == "__main__":
    print("a")
    answer = ["2", "2"]
    # checkKadai(exeKadai(), answer)
    checkKadaiString(exeKadai(), "閏年です")