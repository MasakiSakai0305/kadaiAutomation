with open ("shellScriptMadeByPythonex1.sh", "w") as f:
    f.write("#!/bin/bash\n")
    f.write("echo shellScriptHoge.sh実行\n")
    f.write("gcc hoge.c -o hoge\n")
    f.write("./hoge << EOF\n")
    f.write("100\n")
    f.write("EOF")




from typing import List


#課題ごとの入力内容:複数入力の場合(一回の実行につき複数回入力が行われる)にも対応
inputCommandsKada = List[List[int]]


#基本・発展問題ごとの入力内容
inputCommandsKadais = List[inputCommandsKadai]

"""
studentID: 学籍番号(下二桁),
classNum: 授業の回数(第n回), 
kihonNum: 基本問題の個数, 
hattenNum: 発展問題の個数,
inputCommandsKihon: 基本課題の問題毎の入力内容, 
inputCommandsHatten: 発展課題の問題毎の入力内容
"""
def makeSHFile(studentID: int, classNum: int, kihonNum: int, hattenNum: int, inputCommandsKihon: inputCommandsKadais, inputCommandsHatten: inputCommandsKadais):
    with open("No_{}_AL200{}.sh".format(classNum, studentID), "w") as f:
        f.write("#!/bin/bash\n")
        print(type(f))

        #基本問題の数だけコンパイル
        for kihon in range(1, kihonNum+1):
            f.write("gcc kihon{}-{}-AL200{}.c -o kihon{}-{}-AL200{}\n".format(classNum, kihon, studentID, classNum, kihon, studentID))

        #発展問題の数だけコンパイル
        for hatten in range(1, hattenNum+1):
            f.write("gcc hatten{}-{}-AL200{}.c -o hatten{}-{}-AL200{}\n".format(classNum, hatten, studentID, classNum, hatten, studentID))
        

        #基本問題実行
        for kihon in range(1, kihonNum+1):
            #基本問題1つ毎に入力内容を書き込む
            makeInputCommands(inputCommands=inputCommandsKihon[kihon], studentID=studentID, classNum=classNum, kadaiNum=kihon, f=f)

        #発展問題実行
        for hatten in range(1, hattenNum+1):
            #発展問題1つ毎に入力内容を書き込む
            makeInputCommands(inputCommands=inputCommandsKihon[hatten], studentID=studentID, classNum=classNum, kadaiNum=hatten, f=f)

#標準入力の内容をshファイルに入力(課題ごと)
def makeInputCommands(inputCommands:inputCommandsKadai, studentID: int, classNum: int, kadaiNum: int, f):
    for inputCommand in inputCommands:
        f.write("./kihon{}-{}-AL200{} << EOF\n".format(classNum, kadaiNum, studentID))
        f.write("{}\n".format(inputCommand))
        f.write("EOF")

# def hoge(inputCommandsAll:inputCommandsAll):
#     print(inputCommandsAll)
#     print(inputCommandsAll[0])

if __name__ == "__main__":
    l1 = [[1],[2],[3]]
    l2 = [[4],[5],[6],[7]]
    l3 = [[8],[9],[10],[11]]
    l4 = [[12],[13],[14]]
    kihon  = [l1, l2]
    hatten = [l3, l4]
    makeSHFile(studentID=10, classNum=2, kihonNum=2, hattenNum=2, inputCommandsKihon=kihon, inputCommandsHatten=hatten)
    