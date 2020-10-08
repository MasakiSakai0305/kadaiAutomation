from exeSH import executeKadaiAndGetOutputResult
from exeSH import getStudentID
from exeSH import checkKadai
from exeSH import checkKadaiString
from exeSH import parseJsonAndGetAnswers

import subprocess
import re
from typing import List
import json
import os

class jugyoKadai:
    def __init__(self, jugyoNo, kihonNum, hattenNum):
        #授業の回数(n回目)
        self.jugyoNo = jugyoNo
        #その回の基本課題の数(shファイル作成に使用)
        self.kihonNum = kihonNum
        #発展課題の数(shファイル作成に使用)
        self.hattenNum = hattenNum
        #チェックを終えた課題をリスト化し，重複実行しないようにする（仮）
        self.checkedKadaiList = []
    
    def checkKadaiByExecuteSHFile(self):
        """
        shファイルを実行して課題のチェックを行う関数
        以下の動作を行う．
        1. ディレクトリ内のc言語（学生が提出したもの）を探索
        2. 存在するcファイルに該当するshファイルのみ選択
        3. 選択されたshファイルの実行
        4. 実行した課題の正解・不正解を表示

        """
        answerList = parseJsonAndGetAnswers(kadaiNum = "kihon1")
        os.chdir("scriptAndprogram/")

        outputResult = executeKadaiAndGetOutputResult(shFile = "kihon1-1_24.sh")
        studentID = getStudentID(filename="kihon1-1_24.sh")
        print(outputResult, studentID, answerList)
        checkKadai(outputResult=outputResult, studentID=studentID, answer=answerList, kadaiNum = "kihon1")
        pass
    
    def searchCProgramFile(self, parameter_list):
        """
        ディレクトリ内を探索し，まだチェックしてない課題(cファイル)をリストとして返す

        return
        kadaiFiles: List[str]
        課題のファイル名が格納されているリスト
        """
        pass

if __name__ == "__main__":
    hoge = jugyoKadai(jugyoNo=1, kihonNum=1,hattenNum=0)
    hoge.checkKadaiByExecuteSHFile()